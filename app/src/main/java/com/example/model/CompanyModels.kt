package com.example.model

enum class AgentStatus {
    IDLE, RUNNING, WAITING, THINKING, NEEDS_APPROVAL, ERROR, COMPLETED
}

enum class TaskPriority {
    CRITICAL, HIGH, MEDIUM, LOW
}

enum class RiskLevel {
    LOW, MEDIUM, HIGH
}

data class AgentInfo(
    val name: String,
    val department: String,
    val status: AgentStatus,
    val progress: Int,
    val lastAction: String,
    val icon: String
)

data class CompanyProject(
    val id: String,
    val title: String,
    val objective: String,
    val status: String,
    val progress: Int,
    val activeAgent: String,
    val pipelineStage: String
)

data class CompanyTask(
    val id: String,
    val projectId: String,
    val agent: String,
    val objective: String,
    val status: AgentStatus,
    val priority: TaskPriority
)

data class CompanyApproval(
    val id: String,
    val projectId: String,
    val agent: String,
    val action: String,
    val riskLevel: RiskLevel,
    val reason: String,
    val status: String
)

data class SystemHealth(
    val backend: String = "HEALTHY",
    val database: String = "HEALTHY",
    val workers: String = "RUNNING",
    val aiProvider: String = "Autonomous Engine",
    val activeTasks: Int = 1,
    val totalProjects: Int = 1
)
