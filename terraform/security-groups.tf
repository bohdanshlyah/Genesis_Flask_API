# Web Security Group of VPC
resource "aws_security_group" "workshop_web_sg" {
    name        = "workshop_web_sg"
    vpc_id      = aws_vpc.vpc.id

    tags = {
      "Name"    = "workshop-web-sg"
    }
  
}
# Web Securoty Group Rules
resource "aws_security_group_rule" "allow_ssh" {
    type = "ingress"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    security_group_id = aws_security_group.workshop_web_sg.id
}
resource "aws_security_group_rule" "allow_ssh_out" {
    type = "egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    security_group_id = aws_security_group.workshop_web_sg.id
}
resource "aws_security_group_rule" "allow_http" {
    type = "ingress"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    security_group_id = aws_security_group.workshop_web_sg.id
}

# DB Security Group of VPC
resource "aws_security_group" "workshop_db_sg" {
    name        = "workshop_db_sg"
    vpc_id      = aws_vpc.vpc.id

    tags = {
      "Name"    = "workshop-db-sg"
    }
  
}
# DB Securoty Group Rules
resource "aws_security_group_rule" "allow_db" {
    type = "ingress"
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = [aws_subnet.public_subnet.cidr_block]
    security_group_id = aws_security_group.workshop_db_sg.id
}
resource "aws_security_group_rule" "allow_db_out" {
    type = "egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    security_group_id = aws_security_group.workshop_db_sg.id
}
