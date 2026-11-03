# Lab 01 — Pre-Signed S3 Upload

```
         User Identity
               │
               ▼
       Upload URL Request
               │
               ▼
         URL Generator
               │
       AWS IAM Credentials
               │
               ▼
       Pre-Signed S3 URL
               │
               ▼
          CLI Client
               │
          HTTP PUT
               │
               ▼
          S3 Bucket
               │
               ▼
       Object Verification
```

> Direct-to-S3 single-file upload using pre-signed URLs, with no application server handling file bytes.
