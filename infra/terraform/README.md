# Terraform: IAM for glogs-wordcloud

Provisions a least-privilege service account with `roles/logging.viewer`.

## Usage

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
# edit terraform.tfvars
terraform init
terraform plan
terraform apply
```

## Security notes

- State may contain sensitive data; use a remote backend with encryption and locking.
- Never commit `terraform.tfvars` or `*.tfstate`.
- Prefer Workload Identity over long-lived service account keys.