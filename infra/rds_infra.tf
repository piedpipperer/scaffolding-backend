# rds_infra.tf

# --- Data Sources (to reference existing resources from networking_infra.tf) ---

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [aws_vpc.main.id] # Updated to reference resource directly
  }

  filter {
    name   = "tag:Name"
    values = ["${var.environment}-private-subnet-*"]
  }
}

data "aws_security_group" "rds" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${var.environment}-rds-sg"
  }
}

resource "random_password" "db_password" {
  length           = 16
  special          = true
  override_special = "!@#$%^&*()-_=+"
}

# --- RDS DB Subnet Group ---
resource "aws_db_subnet_group" "main" {
  name       = "${var.environment}-db-subnet-group"
  subnet_ids = data.aws_subnets.private.ids
  description = "DB subnet group for ${var.environment} environment"

  tags = {
    Name        = "${var.environment}-db-subnet-group"
    Environment = var.environment
  }
}

# --- RDS Aurora Serverless Cluster ---
resource "aws_rds_cluster" "main" {
  cluster_identifier      = "${var.environment}-db-cluster"
  engine                  = "aurora-postgresql"
  engine_mode             = "provisioned"
  enable_http_endpoint    = true
  engine_version          = "15.12"
  database_name           = var.app_name
  master_username         = "${var.app_name}user"
  master_password         = random_password.db_password.result
  db_subnet_group_name    = aws_db_subnet_group.main.name
  vpc_security_group_ids  = [data.aws_security_group.rds.id]
  skip_final_snapshot     = true
  apply_immediately       = true # For faster deployment during testing

  serverlessv2_scaling_configuration {
    min_capacity = 0.5
    max_capacity = 16
  }

  tags = {
    Name        = "${var.environment}-db-cluster"
    Environment = var.environment
  }
}

resource "aws_rds_cluster_instance" "main" {
  cluster_identifier = aws_rds_cluster.main.id
  instance_class     = "db.serverless"
  engine             = aws_rds_cluster.main.engine
  engine_version     = aws_rds_cluster.main.engine_version
  publicly_accessible = false

  tags = {
    Name        = "${var.environment}-db-instance"
    Environment = var.environment
  }
}

# --- Secrets Manager Secret for RDS Credentials ---
resource "aws_secretsmanager_secret" "rds_credentials" {
  name        = "${var.environment}/rds/credentials"
  description = "RDS credentials for ${var.environment} environment"

  tags = {
    Environment = var.environment
  }
}

resource "aws_secretsmanager_secret_version" "rds_credentials_version" {
  secret_id     = aws_secretsmanager_secret.rds_credentials.id
  secret_string = jsonencode({
    username = "${var.app_name}user",
    password = random_password.db_password.result,
    engine   = "aurora-postgresql", # Changed to aurora-postgresql
    host     = aws_rds_cluster.main.endpoint, # Changed to cluster endpoint
    port     = aws_rds_cluster.main.port,
    dbClusterIdentifier = aws_rds_cluster.main.id
  })
}

# --- Outputs ---
output "db_cluster_endpoint" {
  description = "The endpoint of the RDS DB cluster."
  value       = aws_rds_cluster.main.endpoint
}

output "db_cluster_port" {
  description = "The port of the RDS DB cluster."
  value       = aws_rds_cluster.main.port
}

output "rds_secret_arn" {
  description = "The ARN of the Secrets Manager secret storing RDS credentials."
  value       = aws_secretsmanager_secret.rds_credentials.arn
}
