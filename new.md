document_parsing_engine/
├── engine/
│   └── document_parsing_engine.py
│
├── app/
│   └── services/
│       ├── section_parsing_service.py
│       ├── normalization_service.py
│       └── validation_service.py
│
├── domain/
│   ├── models/
│   │   ├── bbox.py
│   │   ├── block_item.py
│   │   ├── row.py
│   │   ├── section.py
│   │   └── parse_result.py
│   │
│   ├── layout/
│   │   ├── row_clusterer.py
│   │   └── zone_splitter.py
│   │
│   ├── parsers/
│   │   ├── document/
│   │   │   ├── base_document_parser.py
│   │   │   └── invoice_document_parser.py
│   │   └── section/
│   │       ├── base_section_parser.py
│   │       ├── group_kv_section_parser.py
│   │       └── table_section_parser.py
│   │
│   ├── normalizers/
│   │   └── invoice_normalizer.py
│   │
│   └── validators/
│       └── invoice_validator.py
│
├── presets/
│   └── invoice.py
│
└── utils/
    ├── refs.py
    └── text.py