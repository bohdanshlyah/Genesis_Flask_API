resource "aws_db_subnet_group" "workshop_subnet" {
  name       = "workshop_subnet"
  subnet_ids = [aws_subnet.public_subnet.id, aws_subnet.private_subnet.id]

  tags = {
    Name = "Workshop_db_subnet"
  }
}

resource "aws_db_instance" "workshop" {
  allocated_storage    = 10
  engine               = "mysql"
  engine_version       = "8.0.29"
  instance_class       = "db.t2.micro"
  identifier           = "workshop-1"
  db_name              = "workshop"
  username             = "workshop"
  password             = "workshop"
  skip_final_snapshot  = true
  multi_az = false

  db_subnet_group_name = aws_db_subnet_group.workshop_subnet.id

  vpc_security_group_ids = [
      aws_security_group.workshop_db_sg.id
  ]
}