package com.example.ui.screens

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.model.*
import com.example.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CommandCenterScreen() {
    var activeTab by remember { mutableStateOf("Dashboard") }
    var ceoCommandText by remember { mutableStateOf("RepairShop-v1.2: Scaffolding automated booking flow") }
    var showDirectivesDialog by remember { mutableStateOf(false) }

    var projects by remember {
        mutableStateOf(
            listOf(
                CompanyProject(
                    id = "PROJECT-001",
                    title = "RepairShop-v1.2",
                    objective = "Scaffolding automated booking flow with live quotes & payment integration.",
                    status = "ACTIVE",
                    progress = 90,
                    activeAgent = "security",
                    pipelineStage = "Security Review"
                )
            )
        )
    }

    var agents by remember {
        mutableStateOf(
            listOf(
                AgentInfo("ceo", "Executive Orchestration", AgentStatus.RUNNING, 100, "Orchestrating workflow transitions...", "👑"),
                AgentInfo("developer", "Software Engineering", AgentStatus.RUNNING, 85, "Optimizing Docker manifest...", "⚡"),
                AgentInfo("design", "UI/UX Architecture", AgentStatus.IDLE, 100, "IDLE: Asset delivery confirmed.", "🎨"),
                AgentInfo("security", "Cybersecurity & Audit", AgentStatus.RUNNING, 45, "Scanning OWASP Top 10 vulnerabilities...", "🛡️"),
                AgentInfo("qa", "Quality Assurance", AgentStatus.WAITING, 70, "14-point regression suite queued", "🔍"),
                AgentInfo("sales", "Scope & Commercials", AgentStatus.IDLE, 100, "Milestone scope verified", "💼"),
                AgentInfo("client", "Client Communication", AgentStatus.IDLE, 100, "Client feed sync active", "👤"),
                AgentInfo("deployment", "Release & DevOps", AgentStatus.NEEDS_APPROVAL, 90, "Staging package locked. Needs signoff.", "🚀"),
                AgentInfo("documentation", "Tech Specs & Runbooks", AgentStatus.IDLE, 100, "Auto-generated architecture docs", "📚")
            )
        )
    }

    var tasks by remember {
        mutableStateOf(
            listOf(
                CompanyTask("TASK-001", "PROJECT-001", "ceo", "Architect requirements and plan", AgentStatus.COMPLETED, TaskPriority.HIGH),
                CompanyTask("TASK-002", "PROJECT-001", "design", "Design High Density M3 design system tokens", AgentStatus.COMPLETED, TaskPriority.HIGH),
                CompanyTask("TASK-003", "PROJECT-001", "developer", "Implement HTML5/CSS3/JS app in sandbox", AgentStatus.COMPLETED, TaskPriority.HIGH),
                CompanyTask("TASK-004", "PROJECT-001", "qa", "Run regression verification suite", AgentStatus.COMPLETED, TaskPriority.HIGH),
                CompanyTask("TASK-005", "PROJECT-001", "security", "Security review & CSP validation", AgentStatus.RUNNING, TaskPriority.HIGH),
                CompanyTask("TASK-006", "PROJECT-001", "documentation", "Generate technical README and runbook", AgentStatus.IDLE, TaskPriority.MEDIUM),
                CompanyTask("TASK-007", "PROJECT-001", "deployment", "Deploy production build to live target", AgentStatus.NEEDS_APPROVAL, TaskPriority.CRITICAL)
            )
        )
    }

    var approvals by remember {
        mutableStateOf(
            listOf(
                CompanyApproval(
                    id = "APP-9F3B1A",
                    projectId = "PROJECT-001",
                    agent = "deployment",
                    action = "Deploy production release to live environment",
                    riskLevel = RiskLevel.HIGH,
                    reason = "QA checks and security audit cleared. Production release requested.",
                    status = "PENDING"
                ),
                CompanyApproval(
                    id = "APP-8C2E4D",
                    projectId = "PROJECT-001",
                    agent = "security",
                    action = "Grant elevated CSP network permissions",
                    riskLevel = RiskLevel.MEDIUM,
                    reason = "Backend telemetry requires TLS websocket endpoint.",
                    status = "PENDING"
                )
            )
        )
    }

    val pendingApprovalsCount = approvals.count { it.status == "PENDING" }

    Scaffold(
        topBar = {
            // High Density Header
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(HighDensityBg)
                    .statusBarsPadding()
                    .padding(horizontal = 16.dp, vertical = 12.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        // Avatar Badge (Purple Circle with "K")
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .shadow(2.dp, CircleShape)
                                .clip(CircleShape)
                                .background(HighDensityPrimary),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                "K",
                                color = Color.White,
                                fontWeight = FontWeight.Bold,
                                fontSize = 18.sp
                            )
                        }

                        Column {
                            Text(
                                "Command Center",
                                style = MaterialTheme.typography.titleMedium.copy(
                                    fontWeight = FontWeight.SemiBold,
                                    fontSize = 18.sp,
                                    color = HighDensityTextPrimary
                                )
                            )
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(6.dp)
                            ) {
                                Box(
                                    modifier = Modifier
                                        .size(8.dp)
                                        .clip(CircleShape)
                                        .background(HighDensitySuccess)
                                )
                                Text(
                                    "SYSTEM: OPTIMIZED",
                                    fontSize = 10.sp,
                                    letterSpacing = 1.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = HighDensityTextSecondary.copy(alpha = 0.8f)
                                )
                            }
                        }
                    }

                    // Notification / Refresh Action
                    IconButton(
                        onClick = { /* Refresh status */ },
                        modifier = Modifier
                            .size(44.dp)
                            .clip(CircleShape)
                            .background(HighDensitySurfaceVariant)
                    ) {
                        Icon(
                            imageVector = Icons.Outlined.Notifications,
                            contentDescription = "Notifications",
                            tint = HighDensityTextSecondary,
                            modifier = Modifier.size(22.dp)
                        )
                    }
                }
            }
        },
        bottomBar = {
            // High Density Bottom Navigation Bar
            Surface(
                color = HighDensitySurfaceVariant,
                modifier = Modifier
                    .fillMaxWidth()
                    .navigationBarsPadding()
                    .border(width = 1.dp, color = HighDensityBorder, shape = RoundedCornerShape(0.dp))
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 12.dp, vertical = 8.dp),
                    horizontalArrangement = Arrangement.SpaceAround,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // Dashboard Tab
                    val isDashboard = activeTab == "Dashboard"
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier
                            .clickable { activeTab = "Dashboard" }
                            .padding(4.dp)
                    ) {
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(16.dp))
                                .background(if (isDashboard) HighDensityPrimaryContainer else Color.Transparent)
                                .padding(horizontal = 18.dp, vertical = 4.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Filled.Dashboard,
                                contentDescription = "Dashboard",
                                tint = if (isDashboard) HighDensityOnPrimaryContainer else HighDensityTextSecondary,
                                modifier = Modifier.size(22.dp)
                            )
                        }
                        Spacer(modifier = Modifier.height(2.dp))
                        Text(
                            "Dashboard",
                            fontSize = 11.sp,
                            fontWeight = if (isDashboard) FontWeight.Bold else FontWeight.Medium,
                            color = if (isDashboard) HighDensityOnPrimaryContainer else HighDensityTextSecondary
                        )
                    }

                    // Tasks Tab
                    val isTasks = activeTab == "Tasks"
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier
                            .clickable { activeTab = "Tasks" }
                            .padding(4.dp)
                    ) {
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(16.dp))
                                .background(if (isTasks) HighDensityPrimaryContainer else Color.Transparent)
                                .padding(horizontal = 18.dp, vertical = 4.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.Assignment,
                                contentDescription = "Tasks",
                                tint = if (isTasks) HighDensityOnPrimaryContainer else HighDensityTextSecondary,
                                modifier = Modifier.size(22.dp)
                            )
                        }
                        Spacer(modifier = Modifier.height(2.dp))
                        Text(
                            "Tasks",
                            fontSize = 11.sp,
                            fontWeight = if (isTasks) FontWeight.Bold else FontWeight.Medium,
                            color = if (isTasks) HighDensityOnPrimaryContainer else HighDensityTextSecondary
                        )
                    }

                    // Approvals Tab (with Crimson Badge)
                    val isApprovals = activeTab == "Approvals"
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier
                            .clickable { activeTab = "Approvals" }
                            .padding(4.dp)
                    ) {
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(16.dp))
                                .background(if (isApprovals) HighDensityPrimaryContainer else Color.Transparent)
                                .padding(horizontal = 18.dp, vertical = 4.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            BadgedBox(
                                badge = {
                                    if (pendingApprovalsCount > 0) {
                                        Badge(
                                            containerColor = HighDensityDanger,
                                            contentColor = Color.White
                                        ) {
                                            Text(pendingApprovalsCount.toString(), fontSize = 9.sp, fontWeight = FontWeight.Bold)
                                        }
                                    }
                                }
                            ) {
                                Icon(
                                    imageVector = Icons.Outlined.CheckCircle,
                                    contentDescription = "Approvals",
                                    tint = if (isApprovals) HighDensityOnPrimaryContainer else HighDensityTextSecondary,
                                    modifier = Modifier.size(22.dp)
                                )
                            }
                        }
                        Spacer(modifier = Modifier.height(2.dp))
                        Text(
                            "Approvals",
                            fontSize = 11.sp,
                            fontWeight = if (isApprovals) FontWeight.Bold else FontWeight.Medium,
                            color = if (isApprovals) HighDensityOnPrimaryContainer else HighDensityTextSecondary
                        )
                    }

                    // Config Tab
                    val isConfig = activeTab == "Config"
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier
                            .clickable { activeTab = "Config" }
                            .padding(4.dp)
                    ) {
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(16.dp))
                                .background(if (isConfig) HighDensityPrimaryContainer else Color.Transparent)
                                .padding(horizontal = 18.dp, vertical = 4.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Outlined.Settings,
                                contentDescription = "Config",
                                tint = if (isConfig) HighDensityOnPrimaryContainer else HighDensityTextSecondary,
                                modifier = Modifier.size(22.dp)
                            )
                        }
                        Spacer(modifier = Modifier.height(2.dp))
                        Text(
                            "Config",
                            fontSize = 11.sp,
                            fontWeight = if (isConfig) FontWeight.Bold else FontWeight.Medium,
                            color = if (isConfig) HighDensityOnPrimaryContainer else HighDensityTextSecondary
                        )
                    }
                }
            }
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = { showDirectivesDialog = true },
                containerColor = HighDensityPrimary,
                contentColor = Color.White,
                shape = RoundedCornerShape(16.dp),
                modifier = Modifier
                    .padding(bottom = 8.dp)
                    .size(56.dp)
                    .testTag("floating_action_button")
            ) {
                Icon(
                    imageVector = Icons.Filled.Add,
                    contentDescription = "Add Directive",
                    modifier = Modifier.size(28.dp)
                )
            }
        },
        containerColor = HighDensityBg
    ) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp),
            contentPadding = PaddingValues(top = 4.dp, bottom = 24.dp)
        ) {
            // 1. Hero Active Project Card (Exact High Density Style)
            item {
                val primaryProject = projects.firstOrNull()
                if (primaryProject != null) {
                    HighDensityActiveProjectHero(
                        project = primaryProject
                    )
                }
            }

            // 2. Autonomous Department Agents (High Density 2-Column Grid)
            if (activeTab == "Dashboard" || activeTab == "Config") {
                item {
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                "AUTONOMOUS DEPARTMENTS",
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Black,
                                letterSpacing = 1.sp,
                                color = HighDensityTextSecondary
                            )
                            Text(
                                "9 Active Agents",
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold,
                                color = HighDensityPrimary
                            )
                        }

                        // Render in dense 2-column layout pairs
                        val agentPairs = agents.chunked(2)
                        agentPairs.forEach { pair ->
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.spacedBy(10.dp)
                            ) {
                                Box(modifier = Modifier.weight(1f)) {
                                    HighDensityAgentCard(agent = pair[0])
                                }
                                if (pair.size > 1) {
                                    Box(modifier = Modifier.weight(1f)) {
                                        HighDensityAgentCard(agent = pair[1])
                                    }
                                } else {
                                    Spacer(modifier = Modifier.weight(1f))
                                }
                            }
                        }
                    }
                }
            }

            // 3. Live Telemetry Console (Dark Contrast Box matching design)
            if (activeTab == "Dashboard") {
                item {
                    HighDensityLiveTelemetryBox()
                }
            }

            // 4. Pending Approvals Section
            if ((activeTab == "Dashboard" || activeTab == "Approvals") && approvals.any { it.status == "PENDING" }) {
                item {
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        Text(
                            "PENDING APPROVAL GATES (${pendingApprovalsCount})",
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Black,
                            letterSpacing = 1.sp,
                            color = HighDensityDanger
                        )
                        approvals.filter { it.status == "PENDING" }.forEach { app ->
                            HighDensityApprovalCard(
                                approval = app,
                                onApprove = {
                                    approvals = approvals.map { if (it.id == app.id) it.copy(status = "APPROVED") else it }
                                },
                                onReject = {
                                    approvals = approvals.map { if (it.id == app.id) it.copy(status = "REJECTED") else it }
                                }
                            )
                        }
                    }
                }
            }

            // 5. Persistent Task Queue
            if (activeTab == "Dashboard" || activeTab == "Tasks") {
                item {
                    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                        Text(
                            "PERSISTENT TASK QUEUE",
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Black,
                            letterSpacing = 1.sp,
                            color = HighDensityTextSecondary
                        )
                        tasks.forEach { task ->
                            HighDensityTaskCard(task = task)
                        }
                    }
                }
            }

            // 6. Directive Dispatcher
            item {
                HighDensityDirectiveCard(
                    commandText = ceoCommandText,
                    onCommandChange = { ceoCommandText = it },
                    onDispatch = {
                        if (ceoCommandText.isNotBlank()) {
                            val newProject = CompanyProject(
                                id = "PROJECT-00${projects.size + 1}",
                                title = ceoCommandText.take(24),
                                objective = ceoCommandText,
                                status = "ACTIVE",
                                progress = 20,
                                activeAgent = "ceo",
                                pipelineStage = "Requirements"
                            )
                            projects = listOf(newProject) + projects
                        }
                    }
                )
            }
        }
    }

    // Modal Sheet / Dialog for Quick Directive Creation
    if (showDirectivesDialog) {
        AlertDialog(
            onDismissRequest = { showDirectivesDialog = false },
            title = {
                Text(
                    "New Executive Directive",
                    fontWeight = FontWeight.Bold,
                    color = HighDensityTextPrimary,
                    fontSize = 16.sp
                )
            },
            text = {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(
                        "Dispatch autonomous instructions to the CEO orchestrator:",
                        fontSize = 12.sp,
                        color = HighDensityTextSecondary
                    )
                    OutlinedTextField(
                        value = ceoCommandText,
                        onValueChange = { ceoCommandText = it },
                        modifier = Modifier.fillMaxWidth(),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = HighDensityPrimary,
                            unfocusedBorderColor = HighDensityBorder,
                            focusedTextColor = HighDensityTextPrimary,
                            unfocusedTextColor = HighDensityTextPrimary
                        ),
                        shape = RoundedCornerShape(12.dp)
                    )
                }
            },
            confirmButton = {
                Button(
                    onClick = {
                        if (ceoCommandText.isNotBlank()) {
                            val newProject = CompanyProject(
                                id = "PROJECT-00${projects.size + 1}",
                                title = ceoCommandText.take(24),
                                objective = ceoCommandText,
                                status = "ACTIVE",
                                progress = 10,
                                activeAgent = "ceo",
                                pipelineStage = "Requirements"
                            )
                            projects = listOf(newProject) + projects
                        }
                        showDirectivesDialog = false
                    },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = HighDensityPrimary,
                        contentColor = Color.White
                    ),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text("Dispatch")
                }
            },
            dismissButton = {
                TextButton(onClick = { showDirectivesDialog = false }) {
                    Text("Cancel", color = HighDensityTextSecondary)
                }
            },
            containerColor = HighDensitySurface,
            shape = RoundedCornerShape(20.dp)
        )
    }
}

/**
 * Active Project Hero Card matching the High Density design template
 */
@Composable
fun HighDensityActiveProjectHero(
    project: CompanyProject
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .border(1.dp, HighDensityBorderHighlight, RoundedCornerShape(28.dp)),
        colors = CardDefaults.cardColors(containerColor = HighDensityPrimaryContainer),
        shape = RoundedCornerShape(28.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            // Header Row: Active Project & 90% Progress Badge
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.Top
            ) {
                Column {
                    Text(
                        "ACTIVE PROJECT",
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 1.5.sp,
                        color = HighDensityOnPrimaryContainer.copy(alpha = 0.7f)
                    )
                    Text(
                        project.title,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold,
                        color = HighDensityOnPrimaryContainer
                    )
                }

                Surface(
                    color = HighDensityOnPrimaryContainer,
                    shape = RoundedCornerShape(100.dp)
                ) {
                    Text(
                        "${project.progress}% PROGRESS",
                        color = Color.White,
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
                    )
                }
            }

            // Progress Bar (Track bg-white/40, fill #6750a4)
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(10.dp)
                    .clip(RoundedCornerShape(5.dp))
                    .background(Color.White.copy(alpha = 0.4f))
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(project.progress / 100f)
                        .fillMaxHeight()
                        .clip(RoundedCornerShape(5.dp))
                        .background(HighDensityPrimary)
                )
            }

            // Bottom Row: Current Stage & Overlapping Avatars Stack
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        "Current: ",
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Medium,
                        color = HighDensityTextSecondary
                    )
                    Text(
                        project.pipelineStage,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        color = HighDensityOnPrimaryContainer
                    )
                }

                // Overlapping Avatars Stack
                Row(
                    modifier = Modifier.padding(start = 8.dp)
                ) {
                    Box(
                        modifier = Modifier
                            .size(24.dp)
                            .clip(CircleShape)
                            .background(HighDensityPrimary)
                            .border(2.dp, HighDensityPrimaryContainer, CircleShape)
                    )
                    Box(
                        modifier = Modifier
                            .offset(x = (-6).dp)
                            .size(24.dp)
                            .clip(CircleShape)
                            .background(HighDensitySuccess)
                            .border(2.dp, HighDensityPrimaryContainer, CircleShape)
                    )
                    Box(
                        modifier = Modifier
                            .offset(x = (-12).dp)
                            .size(24.dp)
                            .clip(CircleShape)
                            .background(HighDensityInfo)
                            .border(2.dp, HighDensityPrimaryContainer, CircleShape)
                    )
                }
            }
        }
    }
}

/**
 * Compact High Density Agent Card (Grid Cell)
 */
@Composable
fun HighDensityAgentCard(agent: AgentInfo) {
    val isActive = agent.status == AgentStatus.RUNNING || agent.status == AgentStatus.NEEDS_APPROVAL
    val isNeedsApproval = agent.status == AgentStatus.NEEDS_APPROVAL

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .height(108.dp)
            .border(
                width = if (isNeedsApproval) 1.5.dp else 1.dp,
                color = if (isNeedsApproval) HighDensityPrimary else HighDensityBorder,
                shape = RoundedCornerShape(16.dp)
            ),
        colors = CardDefaults.cardColors(
            containerColor = if (isNeedsApproval) HighDensitySurfaceVariant else HighDensitySurface
        ),
        shape = RoundedCornerShape(16.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(12.dp),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            // Header Row (Agent Name + Pulsing Status Dot/Badge)
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    agent.name.uppercase(),
                    fontSize = 10.sp,
                    fontWeight = FontWeight.Black,
                    color = if (isNeedsApproval) HighDensityPrimary else HighDensityTextSecondary
                )

                if (isNeedsApproval) {
                    Surface(
                        color = HighDensityPrimary,
                        shape = RoundedCornerShape(4.dp)
                    ) {
                        Text(
                            "ACTIVE",
                            fontSize = 8.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color.White,
                            modifier = Modifier.padding(horizontal = 5.dp, vertical = 2.dp)
                        )
                    }
                } else if (agent.status == AgentStatus.RUNNING) {
                    Box(
                        modifier = Modifier
                            .size(8.dp)
                            .clip(CircleShape)
                            .background(HighDensitySuccess)
                    )
                } else {
                    Box(
                        modifier = Modifier
                            .size(8.dp)
                            .clip(CircleShape)
                            .background(HighDensityTextSecondary.copy(alpha = 0.5f))
                    )
                }
            }

            // Subtext Action
            Text(
                text = agent.lastAction,
                fontSize = 11.sp,
                fontWeight = if (isNeedsApproval) FontWeight.Bold else FontWeight.Medium,
                color = HighDensityTextPrimary,
                maxLines = 2,
                lineHeight = 14.sp
            )

            // Mini Progress Bar
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(4.dp)
                    .clip(RoundedCornerShape(2.dp))
                    .background(if (isNeedsApproval) Color.White else HighDensitySurfaceVariant)
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(agent.progress / 100f)
                        .fillMaxHeight()
                        .clip(RoundedCornerShape(2.dp))
                        .background(HighDensityPrimary)
                )
            }
        }
    }
}

/**
 * Live Telemetry Console (Dark container matching Design HTML)
 */
@Composable
fun HighDensityLiveTelemetryBox() {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .height(132.dp),
        colors = CardDefaults.cardColors(containerColor = HighDensityDarkCard),
        shape = RoundedCornerShape(24.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    "LIVE TELEMETRY",
                    fontSize = 10.sp,
                    fontWeight = FontWeight.Bold,
                    letterSpacing = 2.sp,
                    color = Color.White.copy(alpha = 0.5f)
                )
                Text(
                    "WEBSOCKET CONNECTED",
                    fontSize = 9.sp,
                    fontFamily = FontFamily.Monospace,
                    fontWeight = FontWeight.Bold,
                    color = HighDensitySuccess
                )
            }

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f),
                verticalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text("[09:42:01]", fontSize = 10.sp, fontFamily = FontFamily.Monospace, color = HighDensityPrimaryContainer)
                    Text("[QA] PASS: Auth flow validation", fontSize = 10.sp, fontFamily = FontFamily.Monospace, color = HighDensityDarkCardText)
                }
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text("[09:42:15]", fontSize = 10.sp, fontFamily = FontFamily.Monospace, color = HighDensityPrimaryContainer)
                    Text("[SEC] START: Dependency audit", fontSize = 10.sp, fontFamily = FontFamily.Monospace, color = HighDensityDarkCardText)
                }
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text("[09:42:30]", fontSize = 10.sp, fontFamily = FontFamily.Monospace, color = HighDensityPrimaryContainer)
                    Text("[SYS] NODE_ENV=PROD", fontSize = 10.sp, fontFamily = FontFamily.Monospace, color = HighDensitySuccess, fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}

/**
 * Approvals Card styled with High Density theme
 */
@Composable
fun HighDensityApprovalCard(
    approval: CompanyApproval,
    onApprove: () -> Unit,
    onReject: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .border(1.dp, HighDensityBorder, RoundedCornerShape(16.dp)),
        colors = CardDefaults.cardColors(containerColor = HighDensitySurface),
        shape = RoundedCornerShape(16.dp)
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    "SHIELD GATE [${approval.agent.uppercase()}]",
                    color = HighDensityPrimary,
                    fontWeight = FontWeight.Black,
                    fontSize = 11.sp
                )
                Surface(
                    color = HighDensityDanger.copy(alpha = 0.12f),
                    shape = RoundedCornerShape(4.dp)
                ) {
                    Text(
                        "${approval.riskLevel} RISK",
                        color = HighDensityDanger,
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                    )
                }
            }
            Spacer(modifier = Modifier.height(6.dp))
            Text(approval.action, fontWeight = FontWeight.Bold, color = HighDensityTextPrimary, fontSize = 13.sp)
            Text(approval.reason, color = HighDensityTextSecondary, fontSize = 11.sp)
            Spacer(modifier = Modifier.height(10.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(
                    onClick = onApprove,
                    modifier = Modifier.weight(1f).height(38.dp).testTag("approve_btn_${approval.id}"),
                    colors = ButtonDefaults.buttonColors(containerColor = HighDensitySuccess, contentColor = Color.White),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text("✓ APPROVE", fontWeight = FontWeight.Bold, fontSize = 12.sp)
                }
                Button(
                    onClick = onReject,
                    modifier = Modifier.weight(1f).height(38.dp).testTag("reject_btn_${approval.id}"),
                    colors = ButtonDefaults.buttonColors(containerColor = HighDensityDanger, contentColor = Color.White),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text("✗ REJECT", fontWeight = FontWeight.Bold, fontSize = 12.sp)
                }
            }
        }
    }
}

/**
 * Task Row in High Density Theme
 */
@Composable
fun HighDensityTaskCard(task: CompanyTask) {
    Surface(
        color = HighDensitySurface,
        shape = RoundedCornerShape(12.dp),
        modifier = Modifier
            .fillMaxWidth()
            .border(1.dp, HighDensityBorder, RoundedCornerShape(12.dp))
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(task.id, fontSize = 11.sp, color = HighDensityPrimary, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("[${task.agent.uppercase()}]", fontSize = 10.sp, color = HighDensityTextSecondary, fontWeight = FontWeight.SemiBold)
                }
                Text(task.objective, fontSize = 12.sp, color = HighDensityTextPrimary, maxLines = 1)
            }
            Text(
                task.status.name,
                fontSize = 10.sp,
                fontWeight = FontWeight.Bold,
                color = if (task.status == AgentStatus.COMPLETED) HighDensitySuccess else if (task.status == AgentStatus.RUNNING) HighDensityPrimary else HighDensityTextSecondary
            )
        }
    }
}

/**
 * Directive Dispatch Card
 */
@Composable
fun HighDensityDirectiveCard(
    commandText: String,
    onCommandChange: (String) -> Unit,
    onDispatch: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .border(1.dp, HighDensityBorder, RoundedCornerShape(16.dp)),
        colors = CardDefaults.cardColors(containerColor = HighDensitySurface),
        shape = RoundedCornerShape(16.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("⚡", fontSize = 16.sp)
                Spacer(modifier = Modifier.width(6.dp))
                Text(
                    "Executive Directive Box",
                    fontWeight = FontWeight.Bold,
                    color = HighDensityTextPrimary,
                    fontSize = 14.sp
                )
            }
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                "Issue instructions to the CEO orchestrator to launch project task graphs.",
                color = HighDensityTextSecondary,
                fontSize = 11.sp
            )
            Spacer(modifier = Modifier.height(10.dp))
            OutlinedTextField(
                value = commandText,
                onValueChange = onCommandChange,
                modifier = Modifier
                    .fillMaxWidth()
                    .testTag("ceo_command_input"),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = HighDensityPrimary,
                    unfocusedBorderColor = HighDensityBorder,
                    focusedTextColor = HighDensityTextPrimary,
                    unfocusedTextColor = HighDensityTextPrimary,
                    focusedContainerColor = HighDensityBg,
                    unfocusedContainerColor = HighDensityBg
                ),
                shape = RoundedCornerShape(10.dp)
            )
            Spacer(modifier = Modifier.height(10.dp))
            Button(
                onClick = onDispatch,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(44.dp)
                    .testTag("execute_directive_button"),
                colors = ButtonDefaults.buttonColors(
                    containerColor = HighDensityPrimary,
                    contentColor = Color.White
                ),
                shape = RoundedCornerShape(10.dp)
            ) {
                Text("DISPATCH TO CEO AGENT ➔", fontWeight = FontWeight.Bold, fontSize = 12.sp)
            }
        }
    }
}
