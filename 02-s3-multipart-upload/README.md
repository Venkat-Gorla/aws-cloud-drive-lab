# Lab 02 — S3 Multipart Upload

```text
                         Client
                           │
                           │ Initiate Multipart Upload
                           ▼
                     Backend (Lambda)
                           │
                           │ CreateMultipartUpload
                           ▼
                          S3
                           │
                           │ UploadId
                           ▼
                     Backend (Lambda)
                           │
                           │ Generate Pre-Signed URLs
                           │ (Part Numbers)
                           ▼
                         Client
                           │
              ┌────────────┴────────────┐
              │                         │
              │ HTTP PUT                │ HTTP PUT
              ▼                         ▼
         Upload Part 1             Upload Part 2
              │                         │
              ▼                         ▼
              S3                        S3
              │                         │
              │ ETag                    │ ETag
              ▼                         ▼
         Client collects ETags
              │
              │ UploadId + Part Numbers + ETags
              ▼
                     Backend (Lambda)
                           │
                           │ CompleteMultipartUpload
                           ▼
                          S3
                           │
                           │ Assemble uploaded parts
                           ▼
                      Final S3 Object
                           │
                           ▼
                    Object Verification
```

> Direct-to-S3 multipart upload using pre-signed part URLs, with backend-controlled upload initiation and completion.
