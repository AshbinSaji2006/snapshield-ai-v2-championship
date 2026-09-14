# Presentation architecture

## Presentation-friendly version

Use this graphic on slide 4. Solid green components are verified in the current build. The dashed amber branch is a target hardware path, not a completed NPU result.

```mermaid
flowchart LR
  subgraph INPUTS["SUSPICIOUS INPUTS"]
    M[Message]
    U[URL]
    S[Screenshot]
    Q[QR image]
  end

  subgraph LOCAL["LOCAL PREPROCESSING - VERIFIED"]
    V[Validate and normalize]
    O[RapidOCR]
    D[OpenCV QR decode]
  end

  subgraph ENGINES["SPECIALIZED ENGINES - VERIFIED"]
    ML[Text ML / ONNX]
    UF[URL forensics]
    SR[Security rules]
    BD[Brand mismatch]
    PI[PII and redaction]
  end

  F["RISK FUSION\nscore + severity"]
  E["EXPLAINABILITY + ACTION\nevidence + recommendation"]
  DB[(Sanitized local incidents)]
  USER[User]

  M --> V
  U --> V
  S --> V --> O
  Q --> V --> D
  V --> ML
  V --> UF
  V --> PI
  V --> BD
  O --> ML
  O --> UF
  O --> SR
  D --> UF
  D --> BD
  ML & UF & SR & BD & PI --> F --> E --> USER
  E --> DB

  ORT["ONNX Runtime\nCPU verified today"] --> ML
  PA[Provider abstraction] --> ORT
  PA -. "hardware validation pending" .-> QNN["QNN / Snapdragon NPU target"]

  classDef verified fill:#123d32,stroke:#57d7a5,color:#ffffff,stroke-width:2px;
  classDef target fill:#3a2e12,stroke:#f2be55,color:#ffffff,stroke-width:2px,stroke-dasharray:6 4;
  classDef neutral fill:#172026,stroke:#668078,color:#ffffff;
  class V,O,D,ML,UF,SR,BD,PI,F,E,DB,ORT,PA verified;
  class QNN target;
  class M,U,S,Q,USER neutral;
```

Suggested legend:

- **Green / solid:** implemented and verified in the current build.
- **Amber / dashed:** implemented deployment direction awaiting target hardware validation.
- Current provider label: `CPUExecutionProvider`.

## Technical documentation version

```mermaid
sequenceDiagram
  actor User
  participant UI as React/TypeScript UI
  participant API as FastAPI loopback API
  participant Media as Pillow + RapidOCR + OpenCV
  participant O as Orchestrator
  participant ML as TF-IDF + ONNX Runtime
  participant Rules as Text + URL + Brand + PII
  participant Fusion as Risk/Explanation policy
  participant DB as SQLite

  User->>UI: Submit text, URL, or image
  UI->>API: Validated local request
  alt Image input
    API->>Media: MIME, byte, format, pixel validation
    Media->>Media: OCR and QR decode locally
    Media-->>O: Extracted text and QR payloads
  else Text or URL input
    API->>O: Normalized content
  end
  O->>ML: 10,264 float32 TF-IDF features
  ML-->>O: Spam probability + provider + timing
  O->>Rules: Content and decoded destinations
  Rules-->>Fusion: Structured, sanitized findings
  ML-->>Fusion: Supporting model signal
  Fusion-->>O: Score, severity, explanation, actions
  opt Incident persistence enabled
    O->>DB: Hash + sanitized derived metadata
  end
  O-->>UI: Risk + reason + evidence + action
```

### Inference-provider boundary

```mermaid
flowchart TD
  A[Application requests text probability] --> B[TF-IDF preprocessing]
  B --> C{Exact verified QNN report,<br/>provider, filename and SHA-256 match?}
  C -->|No - verified today| CPU[FP32 ONNX / CPUExecutionProvider]
  C -.->|Yes - target hardware only| QNN[QDQ ONNX / QNN HTP<br/>CPU fallback disabled]
  QNN -->|Initialization failure| CPU
  CPU -->|ONNX initialization failure| SK[Local sklearn fallback]
  CPU & QNN & SK --> R[Probability returned to fusion]

  classDef verified fill:#123d32,stroke:#57d7a5,color:#fff;
  classDef target fill:#3a2e12,stroke:#f2be55,color:#fff,stroke-dasharray:6 4;
  class CPU,SK,R verified;
  class QNN target;
```

The QNN branch must remain visually labeled **hardware validation pending** until a named Snapdragon device passes the no-CPU-fallback validation script.

## Privacy architecture comparison

```mermaid
flowchart LR
  subgraph CLOUD["TRADITIONAL REMOTE AI FLOW"]
    P1[Private content] --> NET[Internet / external boundary]
    NET --> REMOTE[Remote AI service]
    REMOTE --> RESULT1[Result]
  end

  subgraph SNAP["SNAPSHIELD CORE FLOW"]
    P2[Private content] --> LOCALAI[Local specialized AI and rules]
    LOCALAI --> RESULT2[Risk + evidence + action]
  end

  classDef risk fill:#3b1f25,stroke:#ff7c86,color:#fff;
  classDef safe fill:#123d32,stroke:#57d7a5,color:#fff;
  class NET,REMOTE risk;
  class P2,LOCALAI,RESULT2 safe;
```

Accurate caption: **SnapShield's core analysis does not require cloud AI or URL network lookup after local installation.** This comparison describes architecture, not a claim that every remote service mishandles data.
