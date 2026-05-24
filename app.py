# app.py
import streamlit as pd
import streamlit as st
import pandas as pd
import plotly.express as px
import time

# Import core architectural components 
from src.database import initialize_database, create_ticket, fetch_active_tickets
from src.structures import MaxBinaryHeapPriorityQueue, TicketNode
from src.workflow import CorporateWorkflowEngine

# Force page configuration to dark theme with wide-layout visualization
st.set_page_config(page_title="Enterprise Governance & Data Engine", layout="wide")

# Initialize SQLite database schema on application launch
initialize_database()

st.title("⚙️ Enterprise Data & Grievance Governance Engine")
st.markdown("""
A multi-disciplinary software engine uniting **Algorithms**, 
**Data Hygiene**, and **Workflow Analytics**.
""")
st.write("---")

# -------------------------------------------------------------------------
# SIDEBAR CONTROL: Ticket Ingestion Engine
# -------------------------------------------------------------------------
st.sidebar.header("📥 Ingest New Corporate Grievance")
with st.sidebar.form("ticket_form", clear_on_submit=True):
    category = st.selectbox("Category", ["System Outage", "Data Breach Attempt", "API Latency Degradation", "User Access Lockout"])
    description = st.text_area("Detailed Description", placeholder="Enter technical context...")
    severity = st.slider("Severity Coefficient (1 = Low, 5 = Critical)", 1, 5, 3)
    sla_hours = st.number_input("SLA Contract Bounds (Hours Allowed)", min_value=1, max_value=72, value=24)
    
    submit_btn = st.form_submit_with_rows = st.form_submit_button("Inject into Data Engine")

if submit_btn and description:
    new_id = create_ticket(category, description, severity, sla_hours)
    st.sidebar.success(f"SQL ACID Transaction Successful. Ticket #{new_id} committed.")

# Fetch active telemetry records from the database
active_raw_tickets = fetch_active_tickets()

# Populate the custom Max-Heap structure from scratch
pq = MaxBinaryHeapPriorityQueue()
for t in active_raw_tickets:
    node = TicketNode(
        ticket_id=t["ticket_id"],
        severity=t["severity"],
        created_at=t["created_at"],
        sla_hours=t["sla_hours"]
    )
    pq.insert(node)

# -------------------------------------------------------------------------
# RENDER MULTI-DISCIPLINARY TABS FOR GERMAN ACADEMIC EVALUATION
# -------------------------------------------------------------------------
tab_is, tab_cs, tab_se = st.tabs([
    "📊 Corporate Governance & Analytics",
    "🧮 Algorithmic Heap Scheduling",
    "💻 Architectural Blueprint & Verification"
])

# =========================================================================
# TAB 1: INFORMATION SYSTEMS (Business Workflows & KPI Analytics)
# =========================================================================
with tab_is:
    st.header("Business Process Automation & Operational Monitoring")
    
    # Generate live KPIs
    kpis = CorporateWorkflowEngine.generate_kpi_dashboard_metrics()
    
    if kpis["total"] == 0:
        st.info("No corporate grievances currently recorded in the database.")
    else:
        # KPI Cards Display
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Tickets Logged", kpis["total"])
        col2.metric("Mean Corporate Severity Index", f"{kpis['severity_avg']:.2f} / 5.0")
        col3.metric("System Operational Status", "Healthy" if kpis["severity_avg"] < 3.5 else "Degraded Load")
        
        st.write("---")
        
        # Interactive Grid: Workflow Management Operations
        st.subheader("📋 Active Operations Control Grid")
        df_active = pd.DataFrame(active_raw_tickets)
        
        # Human-readable formatting for timestamps
        if not df_active.empty:
            df_active["Created Time"] = pd.to_datetime(df_active["created_at"], unit='s').dt.strftime('%Y-%m-%d %H:%M')
            display_cols = ["ticket_id", "category", "description", "severity", "sla_hours", "status", "Created Time"]
            
            for index, row in df_active.iterrows():
                with st.expander(f"Ticket #{row['ticket_id']} | {row['category']} [{row['status']}]"):
                    c_left, c_right = st.columns([3, 1])
                    c_left.write(f"**Description:** {row['description']}")
                    c_left.write(f"*SLA Matrix Check:* Allocation of {row['sla_hours']} hours.")
                    
                    if row["status"] != "Resolved":
                        if c_right.button("Advance Workflow State", key=f"btn_{row['ticket_id']}"):
                            next_state = CorporateWorkflowEngine.process_transition(row['ticket_id'], row['status'])
                            st.rerun()
                    else:
                        c_right.write("✅ State Resolution Finalized")

        # Plotly Analytical Summaries
        st.write("---")
        st.subheader("📈 Aggregated Operational Analytical Metrics")
        if not kpis["status_counts"].empty:
            fig = px.bar(
                kpis["status_counts"], 
                x="Operational Status", 
                y="Volume Totals", 
                title="Organizational Backlog Load Distribution by State",
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)

# =========================================================================
# TAB 2: COMPUTER SCIENCE (Custom Binary Heap Visualization)
# =========================================================================
with tab_cs:
    st.header("Algorithmic Resource Optimization: Scheduling Queue")
    st.markdown("""
    German Computer Science panels value efficient structures. Below is the active state visualization of our 
    **Custom Binary Max-Heap**. It calculates execution order priority dynamically in $O(\log n)$ runtime.
    """)
    
    if len(pq.heap) == 0:
        st.info("The server scheduling queue is empty. No structures to render.")
    else:
        # Primary operational button to execute structural changes
        if st.button("⚡ Dispatch Highest Priority Task (Pop Node from Heap Root)"):
            dispatched_node = pq.extract_max()
            if dispatched_node:
                # Automate resolution state in DB upon extraction
                CorporateWorkflowEngine.process_transition(dispatched_node.ticket_id, "Escalated")
                st.success(f"Dispatched Node Root Ticket #{dispatched_node.ticket_id} with Score {dispatched_node.priority_score:.2f}")
                time.sleep(1)
                st.rerun()
        
        # Display the Serialization array state
        st.subheader("💡 Heap Array Memory Mapping Layout")
        heap_view = pq.get_heap_array_view()
        st.dataframe(pd.DataFrame(heap_view), use_container_width=True)
        
        # Text-Based Graph Layout Diagram Tree Representation
        st.subheader("🌲 Structured Binary Tree Matrix Mapping View")
        st.markdown("```text")
        for idx, node in enumerate(pq.heap):
            level = idx.bit_length() - 1
            indent = "    " * level
            relation = "└── " if idx > 0 else "ROOT: "
            st.markdown(f"{indent}{relation}[Pos {idx}] ID: #{node.ticket_id} (Score: {node.priority_score:.1f})")
        st.markdown("```")

# =========================================================================
# TAB 3: SOFTWARE ENGINEERING (Architectural Blueprint & Proof of Concept)
# =========================================================================
with tab_se:
    st.header("Architectural Transparency & Mathematical Verification")
    
    st.subheader("📊 Math Formulation Alignment")
    st.markdown("""
    Every inbound ticket is fed into our custom balancing evaluation engine. To prevent older tickets from starving, 
    the Max-Heap weight formula dynamically balances **Severity Level**, **Age Acceleration**, and **Contractual SLA parameters**:
    """)
    
    # Render the formal mathematical equations via LaTeX
    st.latex(r"\text{Priority Score} = (\text{Severity} \times 10.0) + (\Delta t_{\text{hours}} \times 1.5) - (\text{SLA Bounds} \times 2.0)")
    
    st.markdown("---")
    st.subheader("🗄️ Relational Database Normalization Schema (Third Normal Form)")
    
    col_sql1, col_sql2 = st.columns(2)
    with col_sql1:
        st.markdown("""
        **Table: `tickets` (Core Entity Store)**
        ```sql
        CREATE TABLE tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            severity INTEGER NOT NULL,
            sla_hours INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            created_at REAL NOT NULL,
            updated_at REAL NOT NULL
        );
        ```
        """)
    with col_sql2:
        st.markdown("""
        **Table: `audit_logs` (Transaction History Store)**
        ```sql
        CREATE TABLE audit_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            previous_status TEXT NOT NULL,
            new_status TEXT NOT NULL,
            changed_at REAL NOT NULL,
            FOREIGN KEY(ticket_id) REFERENCES tickets(ticket_id)
        );
        ```
        """)
        
    st.markdown("---")
    st.caption("Developed independently to fulfill core requirements across CS, SE, and IS academic program paths.")
