import React, { useState, useEffect } from 'react';

const API_BASE = 'http://127.0.0.1:8000/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('CEO');
  const [ceoCommand, setCeoCommand] = useState('Create a modern landing page for a mobile repair business.');
  const [isExecuting, setIsExecuting] = useState(false);
  const [health, setHealth] = useState({
    backend: 'HEALTHY',
    database: 'HEALTHY',
    workers: 'RUNNING',
    websocket: 'ONLINE',
    ai_providers: 'NOT CONFIGURED',
    active_tasks: 0,
    total_projects: 1
  });
  const [agents, setAgents] = useState([
    { name: 'ceo', department: 'Executive Orchestration', status: 'IDLE', progress: 100, last_action: 'Standing by for owner directives' },
    { name: 'sales', department: 'Sales & Requirements', status: 'IDLE', progress: 0, last_action: 'Proposal engine ready' },
    { name: 'client', department: 'Client Communication', status: 'IDLE', progress: 0, last_action: 'Monitoring customer feed' },
    { name: 'design', department: 'UI/UX Architecture', status: 'IDLE', progress: 0, last_action: 'Design token system loaded' },
    { name: 'developer', department: 'Software Engineering', status: 'IDLE', progress: 0, last_action: 'Workspace sandbox secured' },
    { name: 'qa', department: 'Quality Assurance', status: 'IDLE', progress: 0, last_action: 'Test runners armed' },
    { name: 'security', department: 'Cybersecurity & Audit', status: 'IDLE', progress: 0, last_action: 'Scope boundary guards active' },
    { name: 'deployment', department: 'Release & DevOps', status: 'IDLE', progress: 0, last_action: 'Release staging ready' },
    { name: 'documentation', department: 'Technical Documentation', status: 'IDLE', progress: 0, last_action: 'Doc templates ready' },
  ]);
  const [projects, setProjects] = useState([
    {
      id: 'PROJECT-001',
      title: 'Mobile Repair Shop Website',
      objective: 'Create a modern landing page for a mobile repair business.',
      status: 'ACTIVE',
      progress: 65,
      active_agent: 'developer',
      pipeline_stage: 'Development'
    }
  ]);
  const [tasks, setTasks] = useState([
    { id: 'TASK-001', project_id: 'PROJECT-001', agent: 'ceo', objective: 'Architect requirements and plan', status: 'COMPLETED', priority: 'HIGH' },
    { id: 'TASK-002', project_id: 'PROJECT-001', agent: 'design', objective: 'Design responsive UI/UX architecture & theme tokens', status: 'COMPLETED', priority: 'HIGH' },
    { id: 'TASK-003', project_id: 'PROJECT-001', agent: 'developer', objective: 'Implement responsive HTML5/CSS3/JS single page app', status: 'RUNNING', priority: 'HIGH' },
    { id: 'TASK-004', project_id: 'PROJECT-001', agent: 'qa', objective: 'Execute 14-point build verification & regression checks', status: 'PENDING', priority: 'HIGH' },
    { id: 'TASK-005', project_id: 'PROJECT-001', agent: 'security', objective: 'Conduct cybersecurity audit & CSP verification', status: 'PENDING', priority: 'HIGH' },
    { id: 'TASK-006', project_id: 'PROJECT-001', agent: 'documentation', objective: 'Generate technical runbooks and README', status: 'PENDING', priority: 'MEDIUM' },
    { id: 'TASK-007', project_id: 'PROJECT-001', agent: 'deployment', objective: 'Package build and deploy to production', status: 'PENDING', priority: 'HIGH' },
  ]);
  const [approvals, setApprovals] = useState([
    {
      id: 'APP-9F3B1A',
      project_id: 'PROJECT-001',
      agent: 'deployment',
      action: 'Deploy production release to live environment',
      risk_level: 'HIGH',
      reason: 'QA and security audits cleared. Production deployment requested.',
      status: 'PENDING'
    }
  ]);
  const [logs, setLogs] = useState([
    { id: 1, agent: 'ceo', level: 'INFO', message: 'CEO initialized project PROJECT-001 with 7 sequential department milestones', time: '18:50:10' },
    { id: 2, agent: 'design', level: 'INFO', message: 'Generated UI tokens in styles/theme.css (Dark Slate / Electric Blue)', time: '18:50:18' },
    { id: 3, agent: 'developer', level: 'INFO', message: 'Scaffolded index.html and app.js inside authorized sandbox workspace', time: '18:50:29' },
    { id: 4, agent: 'developer', level: 'INFO', message: 'Running build verification and DOM check (80% complete)', time: '18:50:41' }
  ]);

  // Fetch real data from backend
  const fetchData = async () => {
    try {
      const [hRes, pRes, tRes, aRes, lRes, apRes] = await Promise.all([
        fetch(`${API_BASE}/system/health`).then(r => r.json()).catch(() => null),
        fetch(`${API_BASE}/projects`).then(r => r.json()).catch(() => null),
        fetch(`${API_BASE}/tasks`).then(r => r.json()).catch(() => null),
        fetch(`${API_BASE}/agents`).then(r => r.json()).catch(() => null),
        fetch(`${API_BASE}/logs`).then(r => r.json()).catch(() => null),
        fetch(`${API_BASE}/approvals`).then(r => r.json()).catch(() => null)
      ]);
      if (hRes) setHealth(hRes);
      if (pRes && pRes.length > 0) setProjects(pRes);
      if (tRes && tRes.length > 0) setTasks(tRes);
      if (aRes && aRes.length > 0) setAgents(aRes);
      if (apRes) setApprovals(apRes);
      if (lRes && lRes.length > 0) {
        setLogs(lRes.map(l => ({
          ...l,
          time: new Date((l.timestamp || Date.now()) * 1000).toLocaleTimeString()
        })));
      }
    } catch (e) {}
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleExecuteCommand = async () => {
    if (!ceoCommand.trim()) return;
    setIsExecuting(true);
    try {
      await fetch(`${API_BASE}/ceo/command`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: ceoCommand })
      });
      await fetchData();
    } catch (e) {
      // Local demo fallback
      const pid = `PROJECT-00${projects.length + 1}`;
      const newProj = {
        id: pid,
        title: ceoCommand.slice(0, 32),
        objective: ceoCommand,
        status: 'ACTIVE',
        progress: 15,
        active_agent: 'ceo',
        pipeline_stage: 'Requirements'
      };
      setProjects([newProj, ...projects]);
    }
    setIsExecuting(false);
  };

  const handleResolveApproval = async (id, approved) => {
    try {
      await fetch(`${API_BASE}/approvals/${id}/${approved ? 'approve' : 'reject'}`, { method: 'POST' });
      await fetchData();
    } catch (e) {
      setApprovals(approvals.map(a => a.id === id ? { ...a, status: approved ? 'APPROVED' : 'REJECTED' } : a));
    }
  };

  const getStatusBadge = (status) => {
    switch (status?.toUpperCase()) {
      case 'RUNNING': return <span style={{ color: '#24A148', fontWeight: 'bold' }}>🟢 RUNNING</span>;
      case 'WAITING': return <span style={{ color: '#F59E0B', fontWeight: 'bold' }}>🟡 WAITING</span>;
      case 'THINKING': return <span style={{ color: '#0061A4', fontWeight: 'bold' }}>🔵 THINKING</span>;
      case 'NEEDS_APPROVAL': return <span style={{ color: '#B3261E', fontWeight: 'bold' }}>🔴 NEEDS APPROVAL</span>;
      case 'ERROR':
      case 'FAILED': return <span style={{ color: '#B3261E', fontWeight: 'bold' }}>🔴 ERROR</span>;
      case 'COMPLETED': return <span style={{ color: '#24A148', fontWeight: 'bold' }}>✓ COMPLETED</span>;
      default: return <span style={{ color: '#49454F' }}>⚪ IDLE</span>;
    }
  };

  const tabs = [
    'CEO', 'SALES', 'CLIENT', 'DESIGN', 'DEVELOPMENT', 'QA', 'SECURITY', 'DEPLOYMENT',
    'PROJECTS', 'TASKS', 'APPROVALS', 'LOGS', 'MODELS', 'SETTINGS'
  ];

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: '#FDF8F6' }}>
      {/* Sidebar Navigation */}
      <div style={{ width: '260px', background: '#F3EDF7', borderRight: '1px solid #CAC4D0', padding: '1.5rem 1rem', display: 'flex', flexDirection: 'column' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '2rem', paddingLeft: '0.5rem' }}>
          <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: '#6750A4', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.25rem', color: '#fff', fontWeight: 'bold', boxShadow: '0 2px 8px rgba(103, 80, 164, 0.3)' }}>
            K
          </div>
          <div>
            <div style={{ fontWeight: '800', fontSize: '1rem', letterSpacing: '-0.02em', color: '#1D1B1E' }}>Command Center</div>
            <div style={{ fontSize: '0.7rem', color: '#24A148', fontWeight: '700' }}>● SYSTEM: OPTIMIZED</div>
          </div>
        </div>

        <div style={{ fontSize: '0.75rem', fontWeight: '700', color: '#49454F', paddingLeft: '0.5rem', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Departments
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem', flex: 1 }}>
          {tabs.map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{
                textAlign: 'left',
                padding: '0.65rem 0.85rem',
                borderRadius: '8px',
                border: 'none',
                background: activeTab === tab ? '#EADDFF' : 'transparent',
                color: activeTab === tab ? '#21005D' : '#49454F',
                fontWeight: activeTab === tab ? '700' : '500',
                fontSize: '0.85rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
              }}
            >
              <span>{tab}</span>
              {tab === 'APPROVALS' && approvals.filter(a => a.status === 'PENDING').length > 0 && (
                <span style={{ background: '#B3261E', color: '#fff', fontSize: '0.7rem', padding: '0.1rem 0.4rem', borderRadius: '999px', fontWeight: '700' }}>
                  {approvals.filter(a => a.status === 'PENDING').length}
                </span>
              )}
            </button>
          ))}
        </div>

        {/* User / Owner Info */}
        <div style={{ padding: '0.75rem', background: '#FFFFFF', borderRadius: '12px', border: '1px solid #CAC4D0' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '1.1rem' }}>👑</span>
            <div>
              <div style={{ fontSize: '0.8rem', fontWeight: '700', color: '#1D1B1E' }}>Owner / CEO</div>
              <div style={{ fontSize: '0.7rem', color: '#24A148' }}>Full Authorization</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflowY: 'auto' }}>
        {/* Top Header Bar */}
        <div style={{ height: '64px', borderBottom: '1px solid #CAC4D0', background: '#FDF8F6', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 2rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <h2 style={{ margin: 0, fontSize: '1.25rem', fontWeight: '700', color: '#1D1B1E' }}>
              {activeTab} OVERVIEW
            </h2>
            <span style={{ fontSize: '0.8rem', color: '#CAC4D0' }}>|</span>
            <div style={{ fontSize: '0.85rem', color: '#49454F', display: 'flex', gap: '1rem' }}>
              <span>Backend: <b style={{ color: '#24A148' }}>🟢 {health.backend}</b></span>
              <span>Workers: <b style={{ color: '#24A148' }}>🟢 {health.workers}</b></span>
              <span>AI Provider: <b style={{ color: health.ai_providers === 'READY' ? '#24A148' : '#6750A4' }}>{health.ai_providers}</b></span>
            </div>
          </div>
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button
              onClick={fetchData}
              style={{ background: '#F3EDF7', border: '1px solid #CAC4D0', color: '#1D1B1E', padding: '0.45rem 0.9rem', borderRadius: '8px', fontSize: '0.8rem', fontWeight: '600' }}
            >
              🔄 Refresh
            </button>
          </div>
        </div>

        {/* Dynamic View Body */}
        <div style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          
          {/* Executive Command Box (CEO) */}
          {(activeTab === 'CEO' || activeTab === 'PROJECTS') && (
            <div style={{ background: '#FFFFFF', borderRadius: '16px', border: '1px solid #CAC4D0', padding: '1.5rem', boxShadow: '0 2px 12px rgba(0,0,0,0.04)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
                <span style={{ fontSize: '1.25rem' }}>⚡</span>
                <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: '700', color: '#1D1B1E' }}>Executive Company Command Box</h3>
              </div>
              <p style={{ margin: '0 0 1rem 0', fontSize: '0.85rem', color: '#49454F' }}>
                Issue high-level instructions to the CEO Agent. The CEO will analyze the scope, initialize project repositories, create dependency task graphs, and delegate to all 8 specialized departments automatically.
              </p>
              <div style={{ display: 'flex', gap: '1rem' }}>
                <input
                  type="text"
                  value={ceoCommand}
                  onChange={(e) => setCeoCommand(e.target.value)}
                  placeholder="e.g. RepairShop-v1.2: Scaffolding automated booking flow..."
                  style={{ flex: 1, background: '#FDF8F6', border: '1px solid #CAC4D0', borderRadius: '10px', padding: '0.85rem 1rem', color: '#1D1B1E', fontSize: '0.95rem' }}
                />
                <button
                  onClick={handleExecuteCommand}
                  disabled={isExecuting}
                  style={{
                    background: '#6750A4',
                    border: 'none',
                    color: '#FFFFFF',
                    fontWeight: '800',
                    padding: '0.85rem 1.75rem',
                    borderRadius: '10px',
                    fontSize: '0.9rem',
                    boxShadow: '0 2px 10px rgba(103, 80, 164, 0.3)',
                    opacity: isExecuting ? 0.6 : 1
                  }}
                >
                  {isExecuting ? 'ORCHESTRATING...' : 'EXECUTE COMMAND ➔'}
                </button>
              </div>
            </div>
          )}

          {/* Department Agents Status Grid */}
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: '700', color: '#1D1B1E' }}>
                Autonomous Department Agents
              </h3>
              <span style={{ fontSize: '0.8rem', color: '#49454F' }}>Background workers active independently of browser tabs</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1rem' }}>
              {agents.map(ag => (
                <div key={ag.name} style={{ background: '#FFFFFF', border: '1px solid #CAC4D0', borderRadius: '16px', padding: '1rem', display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <div style={{ fontWeight: '800', fontSize: '0.8rem', color: '#49454F', textTransform: 'uppercase' }}>
                        {ag.name}
                      </div>
                      <div style={{ fontSize: '0.75rem', color: '#6750A4', fontWeight: '600' }}>{ag.department}</div>
                    </div>
                    {getStatusBadge(ag.status)}
                  </div>

                  <div style={{ fontSize: '0.8rem', color: '#1D1B1E', fontWeight: '500', minHeight: '34px' }}>
                    {ag.last_action || 'Standing by'}
                  </div>

                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: '#49454F', marginBottom: '0.25rem' }}>
                      <span>Progress</span>
                      <span>{ag.progress}%</span>
                    </div>
                    <div style={{ width: '100%', height: '4px', background: '#F3EDF7', borderRadius: '2px', overflow: 'hidden' }}>
                      <div style={{ width: `${ag.progress}%`, height: '100%', background: '#6750A4', transition: 'width 0.3s ease' }}></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Active Projects & Visual Pipeline */}
          <div>
            <h3 style={{ margin: '0 0 1rem 0', fontSize: '1.1rem', fontWeight: '700', color: '#1D1B1E' }}>
              Project Workspaces & Pipeline Stages
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {projects.map(p => (
                <div key={p.id} style={{ background: '#EADDFF', border: '1px solid #D0BCFF', borderRadius: '28px', padding: '1.5rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                    <div>
                      <div style={{ fontSize: '0.75rem', fontWeight: '800', letterSpacing: '0.1em', textTransform: 'uppercase', color: '#21005D', opacity: 0.7 }}>
                        ACTIVE PROJECT
                      </div>
                      <h4 style={{ margin: '0.2rem 0', fontSize: '1.25rem', color: '#21005D', fontWeight: '800' }}>{p.title}</h4>
                      <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.85rem', color: '#49454F' }}>{p.objective}</p>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <span style={{ background: '#21005D', color: '#FFFFFF', padding: '0.35rem 0.85rem', borderRadius: '999px', fontSize: '0.75rem', fontWeight: '800' }}>
                        {p.progress}% PROGRESS
                      </span>
                    </div>
                  </div>

                  <div style={{ width: '100%', height: '10px', background: 'rgba(255,255,255,0.4)', borderRadius: '5px', overflow: 'hidden', marginBottom: '1rem' }}>
                    <div style={{ width: `${p.progress}%`, height: '100%', background: '#6750A4' }}></div>
                  </div>

                  {/* Visual Pipeline */}
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <div style={{ fontSize: '0.85rem', color: '#49454F' }}>
                      Current: <b style={{ color: '#21005D' }}>{p.pipeline_stage || 'Security Review'}</b>
                    </div>
                    <div style={{ display: 'flex', gap: '-8px' }}>
                      <div style={{ width: '24px', height: '24px', borderRadius: '50%', background: '#6750A4', border: '2px solid #EADDFF' }}></div>
                      <div style={{ width: '24px', height: '24px', borderRadius: '50%', background: '#24A148', border: '2px solid #EADDFF' }}></div>
                      <div style={{ width: '24px', height: '24px', borderRadius: '50%', background: '#0061A4', border: '2px solid #EADDFF' }}></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Pending Approvals & Task Queue */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(380px, 1fr))', gap: '1.5rem' }}>
            {/* Approval Center */}
            <div style={{ background: '#FFFFFF', border: '1px solid #CAC4D0', borderRadius: '16px', padding: '1.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h3 style={{ margin: 0, fontSize: '1rem', fontWeight: '700', color: '#1D1B1E' }}>
                  🛡️ Approval Center
                </h3>
                <span style={{ fontSize: '0.75rem', color: '#49454F' }}>High-Impact Actions Gate</span>
              </div>
              {approvals.length === 0 ? (
                <div style={{ color: '#49454F', fontSize: '0.85rem', textAlign: 'center', padding: '2rem 0' }}>No pending approvals</div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                  {approvals.map(app => (
                    <div key={app.id} style={{ background: '#FDF8F6', border: '1px solid #CAC4D0', borderRadius: '12px', padding: '1rem' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                        <span style={{ color: '#6750A4', fontWeight: '800', fontSize: '0.8rem' }}>{app.agent?.toUpperCase()} AGENT</span>
                        <span style={{ background: '#B3261E', color: '#fff', fontSize: '0.7rem', padding: '0.1rem 0.5rem', borderRadius: '4px', fontWeight: '700' }}>
                          {app.risk_level} RISK
                        </span>
                      </div>
                      <div style={{ fontWeight: '600', fontSize: '0.9rem', color: '#1D1B1E', marginBottom: '0.25rem' }}>{app.action}</div>
                      <div style={{ fontSize: '0.8rem', color: '#49454F', marginBottom: '0.75rem' }}>{app.reason}</div>
                      
                      {app.status === 'PENDING' ? (
                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                          <button
                            onClick={() => handleResolveApproval(app.id, true)}
                            style={{ flex: 1, background: '#24A148', border: 'none', color: '#fff', padding: '0.45rem', borderRadius: '8px', fontWeight: '700', fontSize: '0.8rem' }}
                          >
                            ✓ APPROVE
                          </button>
                          <button
                            onClick={() => handleResolveApproval(app.id, false)}
                            style={{ flex: 1, background: '#B3261E', border: 'none', color: '#fff', padding: '0.45rem', borderRadius: '8px', fontWeight: '700', fontSize: '0.8rem' }}
                          >
                            ✗ REJECT
                          </button>
                        </div>
                      ) : (
                        <span style={{ fontSize: '0.8rem', fontWeight: '700', color: app.status === 'APPROVED' ? '#24A148' : '#B3261E' }}>
                          Status: {app.status}
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Persistent Task Queue */}
            <div style={{ background: '#FFFFFF', border: '1px solid #CAC4D0', borderRadius: '16px', padding: '1.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h3 style={{ margin: 0, fontSize: '1rem', fontWeight: '700', color: '#1D1B1E' }}>
                  📋 Persistent Task Queue
                </h3>
                <span style={{ fontSize: '0.75rem', color: '#49454F' }}>Survives restarts</span>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxHeight: '360px', overflowY: 'auto' }}>
                {tasks.map(t => (
                  <div key={t.id} style={{ background: '#FDF8F6', border: '1px solid #CAC4D0', borderRadius: '10px', padding: '0.75rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span style={{ fontSize: '0.75rem', color: '#6750A4', fontWeight: '800' }}>{t.id}</span>
                        <span style={{ fontSize: '0.7rem', color: '#49454F' }}>[{t.agent?.toUpperCase()}]</span>
                      </div>
                      <div style={{ fontSize: '0.85rem', color: '#1D1B1E', marginTop: '0.2rem' }}>{t.objective}</div>
                    </div>
                    <div>{getStatusBadge(t.status)}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Live Telemetry Console (Dark contrasting box) */}
          <div style={{ background: '#1D1B1E', borderRadius: '24px', padding: '1.25rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <h3 style={{ margin: 0, fontSize: '0.75rem', fontWeight: '700', letterSpacing: '0.2em', textTransform: 'uppercase', color: 'rgba(255,255,255,0.5)' }}>
                LIVE TELEMETRY
              </h3>
              <span style={{ fontSize: '0.75rem', color: '#24A148', fontFamily: 'monospace', fontWeight: 'bold' }}>WEBSOCKET CONNECTED</span>
            </div>
            <div style={{ background: '#121013', borderRadius: '12px', padding: '1rem', fontFamily: 'JetBrains Mono, monospace', fontSize: '0.8rem', color: '#E6E1E5', maxHeight: '180px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
              {logs.map(l => (
                <div key={l.id || Math.random()}>
                  <span style={{ color: '#EADDFF' }}>[{l.time || '18:52:00'}]</span>{' '}
                  <span style={{ color: '#6750A4', fontWeight: '700' }}>[{l.agent?.toUpperCase()}]</span>{' '}
                  <span style={{ color: l.level === 'WARN' ? '#F59E0B' : l.level === 'ERROR' ? '#B3261E' : '#E6E1E5' }}>
                    {l.message}
                  </span>
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
