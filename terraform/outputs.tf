output "vpc_id" {
  value = module.vpc.vpc_id
}

output "public_subnets" {
  value = module.vpc.public_subnets
}

output "s3_bucket_name" {
  value = aws_s3_bucket.report_bucket.bucket
}

output "alb_dns" {
  value = aws_lb.audit_alb.dns_name
}
