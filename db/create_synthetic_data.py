#!/usr/bin/env python3
"""
generate_fundwise_data.py
Hybrid-AI synthetic dataset generator for FundWise (RBI HaRBInger 2025)

Generates:
  /fundwise_dataset/
    /postgres/
      users.csv
      transactions.csv
      behavior_signals.csv
      collusion_graph.csv
      escrow_ledger.csv
      feedback_loop.csv
      trustscore_logs.csv
      audit_trail.csv
      create_tables.sql
      load_data.sql
    /vector_db/
      user_behavior_embeddings.json
      txn_embeddings.json
    README.md

Usage:
  - Configure sizes and toggles below
  - Ensure OPENAI_API_KEY in environment if using OpenAI
  - pip install required packages
"""

import os
import csv
import json
import uuid
import time
import hashlib
import random
from datetime import datetime, timedelta
from faker import Faker
import numpy as np
import networkx as nx
from tqdm import tqdm
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv(dotenv_path="./deployment_config/.env")
print("Loaded API key?", bool(os.getenv("OPENAI_API_KEY")))


# Optional OpenAI integration
USE_OPENAI = True   # set False to skip GPT/embeddings
OPENAI_MODEL = "gpt-4o-mini"  # or text-davinci-003 etc.
OPENAI_EMBED_MODEL = "text-embedding-3-large"
# Install openai package if USE_OPENAI is True
try:
    if USE_OPENAI:
        openai_api_key = os.getenv("OPENAI_API_KEY")

        if not openai_api_key:
            raise RuntimeError("OPENAI_API_KEY not set in environment")

        client = OpenAI(api_key=openai_api_key)

except Exception as e:
    print(f"OpenAI unavailable: {e}. Proceeding without OpenAI.")
    USE_OPENAI = False
    client = None
# ---------- CONFIG ----------
OUTDIR = "/home/ntlpt60/PycharmProjects/startup/Fundwise_iit/dataset"
PG_DIR = os.path.join(OUTDIR, "postgres")
VEC_DIR = os.path.join(OUTDIR, "vector_db")
os.makedirs(PG_DIR, exist_ok=True)
os.makedirs(VEC_DIR, exist_ok=True)

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
F = Faker()
F.seed_instance(SEED)

# sizes (recommended for hackathon)
NUM_USERS = 1000
NUM_TXNS = 30000
NUM_BEHAVIOR = 8000
NUM_EDGES = 6000
NUM_ESCROW = 700
NUM_FEEDBACK = 2500
NUM_TRUST_LOGS = 5000
NUM_AUDIT = 7000
# vector samples
NUM_USER_EMB = NUM_USERS
NUM_TXN_EMB = 10000  # sample of transactions for embeddings

# OpenAI batching
OPENAI_BATCH = 16
OPENAI_SLEEP = 0.5

# ---------- HELPERS ----------
def uid():
    return str(uuid.uuid4())

def now_ts():
    return datetime.utcnow().isoformat()

def recent_datetime(days=90):
    return datetime.utcnow() - timedelta(days=random.randint(0, days), seconds=random.randint(0, 86400))

def hash_chain(prev_hash, payload_str):
    s = (str(prev_hash or "") + "|" + payload_str).encode("utf-8")
    return hashlib.sha256(s).hexdigest()

# ---------- SCHEMAS (for create_tables.sql) ----------
CREATE_TABLES_SQL = """
-- FundWise schema (simplified)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
  user_id UUID PRIMARY KEY,
  name VARCHAR(100),
  kyc_id VARCHAR(50),
  mobile VARCHAR(15),
  email VARCHAR(100),
  device_id VARCHAR(100),
  created_at TIMESTAMP,
  risk_level VARCHAR(20),
  credibility_score FLOAT,
  is_flagged BOOLEAN,
  last_login TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transactions (
  txn_id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(user_id),
  txn_type VARCHAR(30),
  amount DECIMAL(12,2),
  timestamp TIMESTAMP,
  counterparty UUID,
  status VARCHAR(20),
  risk_flag VARCHAR(20),
  channel VARCHAR(30),
  ip_address VARCHAR(45),
  device_id VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS behavior_signals (
  signal_id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(user_id),
  device_pattern_score FLOAT,
  geo_distance_score FLOAT,
  txn_velocity FLOAT,
  anomaly_flag BOOLEAN,
  ip_address VARCHAR(45),
  created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS collusion_graph (
  edge_id UUID PRIMARY KEY,
  user_src UUID REFERENCES users(user_id),
  user_dest UUID REFERENCES users(user_id),
  relationship_type VARCHAR(50),
  weight FLOAT,
  last_interaction TIMESTAMP
);

CREATE TABLE IF NOT EXISTS escrow_ledger (
  block_id SERIAL PRIMARY KEY,
  txn_hash VARCHAR(256),
  sender UUID REFERENCES users(user_id),
  receiver UUID REFERENCES users(user_id),
  amount DECIMAL(12,2),
  prev_hash VARCHAR(256),
  timestamp TIMESTAMP,
  status VARCHAR(20),
  dispute_reason TEXT
);

CREATE TABLE IF NOT EXISTS feedback_loop (
  feedback_id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(user_id),
  target_user_id UUID REFERENCES users(user_id),
  feedback_type VARCHAR(20),
  remarks TEXT,
  timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS trustscore_logs (
  log_id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(user_id),
  score FLOAT,
  components JSONB,
  decision JSONB,
  timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_trail (
  audit_id UUID PRIMARY KEY,
  entity VARCHAR(50),
  entity_id VARCHAR(100),
  action VARCHAR(50),
  performed_by VARCHAR(50),
  details JSONB,
  timestamp TIMESTAMP
);
"""

# ---------- GENERATORS ----------
def generate_users(n):
    users = []
    for _ in range(n):
        u = {
            "user_id": uid(),
            "name": F.name(),
            "kyc_id": f"{F.bothify(text='PAN?????')}"[:50],
            "mobile": F.msisdn()[:15],
            "email": F.free_email(),
            "device_id": str(uuid.uuid4()),
            "created_at": recent_datetime(365).isoformat(),
            "risk_level": random.choices(["low","medium","high"], weights=[0.8,0.15,0.05])[0],
            "credibility_score": round(random.random(), 4),
            "is_flagged": False,
            "last_login": recent_datetime(30).isoformat()
        }
        users.append(u)
    return users

def generate_transactions(users, n):
    txns = []
    user_ids = [u["user_id"] for u in users]
    channels = ["UPI","CARD","WALLET","NETBANKING","AGENT"]
    statuses = ["success", "pending", "failed"]
    for _ in range(n):
        uid_choice = random.choice(user_ids)
        amount = round(max(1.0, np.random.exponential(scale=200)), 2)
        txn = {
            "txn_id": uid(),
            "user_id": uid_choice,
            "txn_type": random.choices(["deposit","withdrawal","transfer","escrow"], weights=[0.4,0.2,0.3,0.1])[0],
            "amount": amount,
            "timestamp": recent_datetime(90).isoformat(),
            "counterparty": random.choice(user_ids + [None]),
            "status": random.choices(statuses, weights=[0.95,0.03,0.02])[0],
            "risk_flag": None,
            "channel": random.choice(channels),
            "ip_address": F.ipv4_private(),
            "device_id": str(uuid.uuid4())
        }
        txns.append(txn)
    return txns

def generate_behavior_signals(users, n):
    signals = []
    user_ids = [u["user_id"] for u in users]
    for _ in range(n):
        uid_choice = random.choice(user_ids)
        s = {
            "signal_id": uid(),
            "user_id": uid_choice,
            "device_pattern_score": round(random.random(), 4),
            "geo_distance_score": round(random.random(), 4),
            "txn_velocity": round(random.expovariate(1/0.5), 4),
            "anomaly_flag": False,
            "ip_address": F.ipv4_private(),
            "created_at": recent_datetime(30).isoformat()
        }
        # Mark some anomalies
        if random.random() < 0.02:
            s["anomaly_flag"] = True
        signals.append(s)
    return signals

def generate_collusion_graph(users, edges):
    user_ids = [u["user_id"] for u in users]
    G = nx.Graph()
    G.add_nodes_from(user_ids)
    # Add community clusters + some rings
    # Make a few dense clusters (fraud rings)
    rings = []
    for _ in range(max(3, int(len(users)/300))):
        ring_size = random.randint(4, 12)
        ring = random.sample(user_ids, ring_size)
        rings.append(ring)
        for i in range(len(ring)):
            for j in range(i+1, len(ring)):
                G.add_edge(ring[i], ring[j], weight=round(random.random(),3), relationship_type=random.choice(["frequent_txn","shared_wallet","shared_ip"]))
    # Add random edges
    while G.number_of_edges() < edges:
        a, b = random.sample(user_ids, 2)
        if G.has_edge(a,b): continue
        G.add_edge(a, b, weight=round(random.random(),3), relationship_type=random.choice(["frequent_txn","shared_wallet","shared_ip","device_link"]))
    # produce edge list
    edges_list = []
    for u,v,data in G.edges(data=True):
        edges_list.append({
            "edge_id": uid(),
            "user_src": u,
            "user_dest": v,
            "relationship_type": data.get("relationship_type", "frequent_txn"),
            "weight": data.get("weight", 1.0),
            "last_interaction": recent_datetime(60).isoformat()
        })
    return edges_list

def generate_escrow_ledger(txns, n):
    ledger = []
    prev_hash = None
    sample_txns = random.sample(txns, min(n, len(txns)))
    for t in sample_txns:
        payload = f"{t['txn_id']}|{t['user_id']}|{t['amount']}|{t['timestamp']}"
        txn_hash = hash_chain(prev_hash, payload)
        entry = {
            "block_id": None,  # fill sequentially later
            "txn_hash": txn_hash,
            "sender": t["user_id"],
            "receiver": t["counterparty"] or t["user_id"],
            "amount": t["amount"],
            "prev_hash": prev_hash,
            "timestamp": recent_datetime(30).isoformat(),
            "status": random.choice(["held","released","disputed"]),
            "dispute_reason": None
        }
        if entry["status"] == "disputed":
            entry["dispute_reason"] = random.choice(["payer_claim","duplicate_txn","identity_mismatch"])
        ledger.append(entry)
        prev_hash = txn_hash
    # assign block ids
    for i, e in enumerate(ledger, start=1):
        e["block_id"] = i
    return ledger

def generate_feedback(users, n):
    feedbacks = []
    user_ids = [u["user_id"] for u in users]
    for _ in range(n):
        a, b = random.sample(user_ids,2)
        f = {
            "feedback_id": uid(),
            "user_id": a,
            "target_user_id": b,
            "feedback_type": random.choices(["green","red"], weights=[0.9,0.1])[0],
            "remarks": None,
            "timestamp": recent_datetime(60).isoformat()
        }
        if random.random() < 0.1:
            f["remarks"] = F.sentence(nb_words=8)
        feedbacks.append(f)
    return feedbacks

def generate_trustscore_logs(users, n):
    logs = []
    user_ids = [u["user_id"] for u in users]
    for _ in range(n):
        uid_choice = random.choice(user_ids)
        comps = {
            "velocity": round(random.random(),4),
            "gnn": round(random.random(),4),
            "anomaly": round(random.random(),4),
            "rules": round(random.random(),4)
        }
        score = max(0.0, min(100.0, 100.0 * (1 - (comps["velocity"]*0.2 + comps["gnn"]*0.35 + comps["anomaly"]*0.35))))
        logs.append({
            "log_id": uid(),
            "user_id": uid_choice,
            "score": round(score,2),
            "components": json.dumps(comps),
            "decision": json.dumps({"flagged": score < 40, "reason": "composite_score"}),
            "timestamp": recent_datetime(90).isoformat()
        })
    return logs

def generate_audit_trail(users, txns, n):
    audits = []
    entities = ["users","transactions","trustscore_logs","escrow_ledger","feedback_loop"]
    for _ in range(n):
        ent = random.choice(entities)
        ent_id = uid() if ent!="transactions" else random.choice(txns)["txn_id"]
        audits.append({
            "audit_id": uid(),
            "entity": ent,
            "entity_id": ent_id,
            "action": random.choice(["create","update","delete","flag","override"]),
            "performed_by": random.choice(["system","admin",random.choice(users)["user_id"]]),
            "details": json.dumps({"note": F.sentence(nb_words=6)}),
            "timestamp": recent_datetime(120).isoformat()
        })
    return audits

# ---------- OpenAI helpers (if enabled) ----------
def gpt_generate_collusion_description(cluster_users):
    """Use OpenAI to generate a short human-friendly description of a collusion cluster."""
    if not USE_OPENAI:
        return f"Collusion cluster with {len(cluster_users)} suspicious accounts."
    prompt = f"Write a 2-sentence audit-friendly description for a collusion cluster of {len(cluster_users)} users. Example user_ids: {cluster_users[:5]} ... Keep it formal and concise."
    try:
        resp = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=120
                )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI GPT error:", e)
        return f"Collusion cluster with {len(cluster_users)} suspicious accounts."

def openai_embed_texts(texts, batch_size=OPENAI_BATCH):
    if not USE_OPENAI:
        # fallback: generate random vectors (consistent)
        return [np.round(np.random.normal(size=768).tolist(), 6) for _ in range(len(texts))]
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        try:
            resp = client.embeddings.create(
                model=OPENAI_EMBED_MODEL,
                input=batch
                )
            embeddings.extend([item.embedding for item in resp.data])
            time.sleep(OPENAI_SLEEP)
        except Exception as e:
            print("OpenAI embedding error:", e)
            # fallback to random
            embeddings.extend([np.round(np.random.normal(size=768).tolist(), 6) for _ in batch])
    return embeddings

# ---------- EXPORTERS ----------
def write_csv(path, rows, headers):
    with open(path, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in rows:
            # flatten any None to empty strings for CSV
            clean = {k: ("" if r.get(k) is None else r.get(k)) for k in headers}
            writer.writerow(clean)

def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, default=str)

# ---------- MAIN ----------
def main():
    print("Generating users...")
    users = generate_users(NUM_USERS)
    print("Generating transactions...")
    txns = generate_transactions(users, NUM_TXNS)
    print("Generating behavior signals...")
    behaviors = generate_behavior_signals(users, NUM_BEHAVIOR)
    print("Generating collusion graph edges...")
    edges = generate_collusion_graph(users, NUM_EDGES)
    print("Generating escrow ledger...")
    ledger = generate_escrow_ledger(txns, NUM_ESCROW)
    print("Generating feedback entries...")
    feedbacks = generate_feedback(users, NUM_FEEDBACK)
    print("Generating trustscore logs...")
    logs = generate_trustscore_logs(users, NUM_TRUST_LOGS)
    print("Generating audit trail entries...")
    audits = generate_audit_trail(users, txns, NUM_AUDIT)

    # If USE_OPENAI: generate cluster descriptions (optional)
    cluster_descs = []
    if USE_OPENAI:
        # find some dense subgraphs (fraud rings) and describe
        G = nx.Graph()
        G.add_nodes_from([u["user_id"] for u in users])
        for e in edges[:min(1000,len(edges))]:
            G.add_edge(e["user_src"], e["user_dest"])
        # find communities
        comps = list(nx.algorithms.community.greedy_modularity_communities(G))
        for c in comps[:10]:
            sample = list(c)[:20]
            d = gpt_generate_collusion_description(sample)
            cluster_descs.append({"members": sample, "description": d})

    # Embeddings generation
    # Build user textual contexts for embeddings
    print("Preparing user textual contexts for embeddings...")
    user_texts = []
    for u in users:
        txt = f"User {u['name']}, kyc:{u['kyc_id']}, risk:{u['risk_level']}, credibility:{u['credibility_score']:.3f}"
        user_texts.append(txt)
    print("Generating user embeddings (may call OpenAI)...")
    user_embeddings = openai_embed_texts(user_texts)  # list of vectors

    # Transaction embeddings: sample some txns
    print("Preparing txn texts for embeddings...")
    txn_sample = random.sample(txns, min(NUM_TXN_EMB, len(txns)))
    txn_texts = [f"Txn {t['txn_id']} user {t['user_id']} amount {t['amount']} channel {t['channel']}" for t in txn_sample]
    print("Generating txn embeddings (may call OpenAI)...")
    txn_embeddings = openai_embed_texts(txn_texts)

    # write CSVs
    print("Writing CSVs...")
    # users
    users_path = os.path.join(PG_DIR, "users.csv")
    write_csv(users_path, users, ["user_id","name","kyc_id","mobile","email","device_id","created_at","risk_level","credibility_score","is_flagged","last_login"])

    txns_path = os.path.join(PG_DIR, "transactions.csv")
    write_csv(txns_path, txns, ["txn_id","user_id","txn_type","amount","timestamp","counterparty","status","risk_flag","channel","ip_address","device_id"])

    beh_path = os.path.join(PG_DIR, "behavior_signals.csv")
    write_csv(beh_path, behaviors, ["signal_id","user_id","device_pattern_score","geo_distance_score","txn_velocity","anomaly_flag","ip_address","created_at"])

    edges_path = os.path.join(PG_DIR, "collusion_graph.csv")
    write_csv(edges_path, edges, ["edge_id","user_src","user_dest","relationship_type","weight","last_interaction"])

    escrow_path = os.path.join(PG_DIR, "escrow_ledger.csv")
    write_csv(escrow_path, ledger, ["block_id","txn_hash","sender","receiver","amount","prev_hash","timestamp","status","dispute_reason"])

    fb_path = os.path.join(PG_DIR, "feedback_loop.csv")
    write_csv(fb_path, feedbacks, ["feedback_id","user_id","target_user_id","feedback_type","remarks","timestamp"])

    logs_path = os.path.join(PG_DIR, "trustscore_logs.csv")
    write_csv(logs_path, logs, ["log_id","user_id","score","components","decision","timestamp"])

    audit_path = os.path.join(PG_DIR, "audit_trail.csv")
    write_csv(audit_path, audits, ["audit_id","entity","entity_id","action","performed_by","details","timestamp"])

    # create SQL files
    create_sql_path = os.path.join(PG_DIR, "create_tables.sql")
    with open(create_sql_path, "w", encoding="utf-8") as f:
        f.write(CREATE_TABLES_SQL)

    load_sql_path = os.path.join(PG_DIR, "load_data.sql")
    with open(load_sql_path, "w", encoding="utf-8") as f:
        f.write("-- Use psql or COPY to load CSVs\n")
        f.write("BEGIN;\n")
        f.write(f"COPY users FROM '{os.path.abspath(users_path)}' CSV HEADER;\n")
        f.write(f"COPY transactions FROM '{os.path.abspath(txns_path)}' CSV HEADER;\n")
        f.write(f"COPY behavior_signals FROM '{os.path.abspath(beh_path)}' CSV HEADER;\n")
        f.write(f"COPY collusion_graph FROM '{os.path.abspath(edges_path)}' CSV HEADER;\n")
        f.write(f"COPY escrow_ledger FROM '{os.path.abspath(escrow_path)}' CSV HEADER;\n")
        f.write(f"COPY feedback_loop FROM '{os.path.abspath(fb_path)}' CSV HEADER;\n")
        f.write(f"COPY trustscore_logs FROM '{os.path.abspath(logs_path)}' CSV HEADER;\n")
        f.write(f"COPY audit_trail FROM '{os.path.abspath(audit_path)}' CSV HEADER;\n")
        f.write("COMMIT;\n")

    # write embeddings JSON for vector DB
    print("Writing vector DB JSONs...")
    user_vecs = []
    for u, emb in zip(users, user_embeddings):
        user_vecs.append({"user_id": u["user_id"], "embedding": emb, "source": "gpt-hybrid", "timestamp": now_ts()})
    write_json(os.path.join(VEC_DIR, "user_behavior_embeddings.json"), user_vecs)

    txn_vecs = []
    for t, emb in zip(txn_sample, txn_embeddings):
        txn_vecs.append({"txn_id": t["txn_id"], "embedding": emb, "source": "gpt-hybrid", "timestamp": now_ts()})
    write_json(os.path.join(VEC_DIR, "txn_embeddings.json"), txn_vecs)

    # README
    with open(os.path.join(OUTDIR, "README.md"), "w", encoding="utf-8") as f:
        f.write("# FundWise Dataset\n\n")
        f.write("Generated by generate_fundwise_data.py\n\n")
        f.write(f"Users: {len(users)}\\nTransactions: {len(txns)}\\nBehavior signals: {len(behaviors)}\\nEdges: {len(edges)}\\nEscrow: {len(ledger)}\\nFeedback: {len(feedbacks)}\\nTrust logs: {len(logs)}\\nAudit: {len(audits)}\\n")

    print("Done. Files written to:", os.path.abspath(OUTDIR))


if __name__ == "__main__":
    main()
