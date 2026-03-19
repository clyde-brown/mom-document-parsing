"""세그먼트 버킷 유틸: 버킷 없는 세그먼트 목록, 다수 테이블 여부 판별."""


def segments_without_buckets(seg) -> list[str]:
    """allowed_segments 중 버킷(매핑된 블록)이 없는 세그먼트 이름 목록을 반환."""
    allowed = set(seg.allowed_segments)
    bucket_names = {b.segment_name for b in seg.segment_buckets}
    return sorted(allowed - bucket_names)


def has_multiple_tables_in_any_bucket(seg, blocks: list) -> bool:
    """한 버킷이라도 테이블 블록이 2개 이상이면 True."""
    ref_to_block = {getattr(b, "ref", None): b for b in blocks if getattr(b, "ref", None)}
    for bucket in seg.segment_buckets:
        table_count = 0
        for ref in getattr(bucket, "block_refs", []):
            block = ref_to_block.get(ref)
            if block is not None and getattr(block, "content_type", "") == "table":
                table_count += 1
                if table_count >= 2:
                    return True
    return False
