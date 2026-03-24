# Terraform Infrastructure

This module provisions the base cloud resources required by **London Transport Analytics**.

## Provisioned Resources

- **Google Cloud Storage bucket** for the raw data lake
- **BigQuery dataset** for downstream warehouse and analytics tables

## Files

- `main.tf` -> provider and resource definitions
- `variables.tf` -> input variables
- `outputs.tf` -> resource outputs
- `terraform.tfvars.example` -> example variable file
- `setup.ps1` -> helper script for credentials setup
- `deploy.ps1` -> helper script for Terraform init and apply

## Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/downloads)
- Google Cloud SDK (`gcloud`)
- A GCP service account with permissions for:
  - `Storage Admin` or equivalent bucket creation access
  - `BigQuery Admin` or equivalent dataset creation access

## Authentication

Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to your service account JSON path.

Example:

```powershell
.\setup.ps1 -CredentialsPath "C:\path\to\service-account.json"
```

## Configuration

Create a working variable file from the example:

```powershell
Copy-Item terraform.tfvars.example terraform.tfvars
```

Then update:

- `project`
- `region`
- `location`
- `gcs_bucket_name`
- `bq_dataset_name`

## Deploy Infrastructure

```powershell
.\deploy.ps1
```

Or run Terraform manually:

```powershell
terraform init
terraform plan
terraform apply
```

## Cleanup

```powershell
terraform destroy
```

## Notes

- The bucket name must be globally unique.
- After deployment, align the bucket name, project ID, and location with the values used in the `Kestra` KV store.
