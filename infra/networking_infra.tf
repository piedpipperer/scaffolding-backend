# networking_infra.tf

# --- Variables ---
variable "environment" {
  description = "The environment name (e.g., dev, prod)."
  type        = string
  default     = "troubleshoot"
}

variable "vpc_cidr" {
  description = "The CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "A list of CIDR blocks for the public subnets."
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "A list of CIDR blocks for the private subnets."
  type        = list(string)
  default     = ["10.0.11.0/24", "10.0.12.0/24"]
}

variable "db_port" {
  description = "The port for the database (e.g., 5432 for PostgreSQL, 3306 for MySQL)."
  type        = number
  default     = 5432 # Default for PostgreSQL
}

# --- VPC ---
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "${var.environment}-vpc"
    Environment = var.environment
  }
}

# --- Internet Gateway ---
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name        = "${var.environment}-igw"
    Environment = var.environment
  }
}

# --- Public Subnets ---
resource "aws_subnet" "public" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true # Public subnets need public IPs for NAT Gateways

  tags = {
    Name        = "${var.environment}-public-subnet-${count.index + 1}"
    Environment = var.environment
  }
}

# --- Private Subnets ---
resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name        = "${var.environment}-private-subnet-${count.index + 1}"
    Environment = var.environment
  }
}

# --- Elastic IPs for NAT Gateways ---
resource "aws_eip" "nat_gateway_eip" {
  count = length(var.public_subnet_cidrs)


  tags = {
    Name        = "${var.environment}-nat-eip-${count.index + 1}"
    Environment = var.environment
  }
}

# --- NAT Gateways ---
resource "aws_nat_gateway" "main" {
  count         = length(var.public_subnet_cidrs)
  allocation_id = aws_eip.nat_gateway_eip[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = {
    Name        = "${var.environment}-nat-gateway-${count.index + 1}"
    Environment = var.environment
  }
  # Ensure the NAT Gateway is created after the EIP and public subnet
  depends_on = [aws_internet_gateway.main]
}

# --- Route Tables ---

# Public Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name        = "${var.environment}-public-rt"
    Environment = var.environment
  }
}

# Private Route Tables (one per NAT Gateway)
resource "aws_route_table" "private" {
  count  = length(var.private_subnet_cidrs)
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }

  tags = {
    Name        = "${var.environment}-private-rt-${count.index + 1}"
    Environment = var.environment
  }
}

# --- Route Table Associations ---

# Public Subnet Associations
resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Private Subnet Associations
resource "aws_route_table_association" "private" {
  count          = length(aws_subnet.private)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

# --- Security Groups ---

# Security Group for RDS
resource "aws_security_group" "rds" {
  name        = "${var.environment}-rds-sg"
  description = "Allow inbound traffic to RDS from Lambda"
  vpc_id      = aws_vpc.main.id



  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # All protocols
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name        = "${var.environment}-rds-sg"
    Environment = var.environment
  }
}

# Security Group for Lambda
resource "aws_security_group" "lambda" {
  name        = "${var.environment}-lambda-sg"
  description = "Allow outbound traffic from Lambda to RDS and internet"
  vpc_id      = aws_vpc.main.id

  # Ingress rules (Lambda typically doesn't need inbound from internet)
  # Add specific ingress rules if Lambda needs to be invoked by specific sources (e.g., ALB, API Gateway)
  # For now, no specific ingress rules are added, assuming invocation is internal or through other services.



  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # All protocols
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic to internet"
  }

  tags = {
    Name        = "${var.environment}-lambda-sg"
    Environment = var.environment
  }
}

# --- Data Source for Availability Zones ---
data "aws_availability_zones" "available" {
  state = "available"
}

# --- Security Group Rules to break circular dependency ---

# Allow RDS ingress from Lambda SG
resource "aws_security_group_rule" "rds_ingress_from_lambda" {
  type                     = "ingress"
  from_port                = var.db_port
  to_port                  = var.db_port
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.lambda.id
  security_group_id        = aws_security_group.rds.id
  description              = "Allow traffic from Lambda SG to RDS"
}

# Allow Lambda egress to RDS SG
resource "aws_security_group_rule" "lambda_egress_to_rds" {
  type                     = "egress"
  from_port                = var.db_port
  to_port                  = var.db_port
  protocol                 = "tcp"
  cidr_blocks = [aws_vpc.main.cidr_block]
  security_group_id        = aws_security_group.lambda.id
  description              = "Allow traffic from Lambda SG to RDS"
}


# --- VPC Endpoint for Secrets Manager ---
resource "aws_vpc_endpoint" "secrets_manager" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.${data.aws_region.current.name}.secretsmanager"
  vpc_endpoint_type = "Interface"

  private_dns_enabled = true

  subnet_ids = aws_subnet.private[*].id

  security_group_ids = [aws_security_group.lambda.id]

  tags = {
    Name        = "${var.environment}-secrets-manager-endpoint"
    Environment = var.environment
  }
}


resource "aws_security_group_rule" "lambda_to_secrets_manager_endpoint" {
  type                     = "ingress"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.lambda.id
  security_group_id        = aws_security_group.lambda.id # The endpoint uses the same SG
  description              = "Allow Lambda to access Secrets Manager VPC endpoint"
}

# --- Data Source for current region ---
data "aws_region" "current" {}

# --- Outputs ---
output "vpc_id" {
  description = "The ID of the newly created VPC."
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "A list of IDs of the public subnets."
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "A list of IDs of the private subnets."
  value       = aws_subnet.private[*].id
}

output "rds_security_group_id" {
  description = "The ID of the security group for RDS."
  value       = aws_security_group.rds.id
}

output "lambda_security_group_id" {
  description = "The ID of the security group for Lambda."
  value       = aws_security_group.lambda.id
}
