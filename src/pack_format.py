# by claude
def get_pack_format(version: str, pack_type: str = "resource") -> int | float | None:
    """
    Get the pack_format value for a given Minecraft Java Edition version.

    Args:
        version: Minecraft version string (e.g. "1.20.1", "1.21.9")
        pack_type: "resource" or "data"

    Returns:
        pack_format value, or None if the version is not found
    """

    RESOURCE_PACK_FORMATS = [
        ((1, 6, 1), (1, 8, 9), 1),
        ((1, 9, 0), (1, 10, 2), 2),
        ((1, 11, 0), (1, 12, 2), 3),
        ((1, 13, 0), (1, 14, 4), 4),
        ((1, 15, 0), (1, 16, 1), 5),
        ((1, 16, 2), (1, 16, 5), 6),
        ((1, 17, 0), (1, 17, 1), 7),
        ((1, 18, 0), (1, 18, 2), 8),
        ((1, 19, 0), (1, 19, 2), 9),
        ((1, 19, 3), (1, 19, 3), 12),
        ((1, 19, 4), (1, 19, 4), 13),
        ((1, 20, 0), (1, 20, 1), 15),
        ((1, 20, 2), (1, 20, 2), 18),
        ((1, 20, 3), (1, 20, 4), 22),
        ((1, 20, 5), (1, 20, 6), 32),
        ((1, 21, 0), (1, 21, 1), 34),
        ((1, 21, 2), (1, 21, 3), 42),
        ((1, 21, 4), (1, 21, 4), 46),
    ]

    DATA_PACK_FORMATS = [
        ((1, 13, 0), (1, 14, 4), 4),
        ((1, 15, 0), (1, 16, 1), 5),
        ((1, 16, 2), (1, 16, 5), 6),
        ((1, 17, 0), (1, 17, 1), 7),
        ((1, 18, 0), (1, 18, 1), 8),
        ((1, 18, 2), (1, 18, 2), 9),
        ((1, 19, 0), (1, 19, 3), 10),
        ((1, 19, 4), (1, 19, 4), 12),
        ((1, 20, 0), (1, 20, 1), 15),
        ((1, 20, 2), (1, 20, 2), 18),
        ((1, 20, 3), (1, 20, 4), 26),
        ((1, 20, 5), (1, 20, 6), 41),
        ((1, 21, 0), (1, 21, 1), 48),
        ((1, 21, 2), (1, 21, 3), 57),
        ((1, 21, 4), (1, 21, 4), 61),
        ((1, 21, 5), (1, 21, 5), 71),
        ((1, 21, 6), (1, 21, 6), 80),
        ((1, 21, 7), (1, 21, 8), 81),
        ((1, 21, 9), (1, 21, 10), 88.0),
        ((1, 21, 11), (1, 21, 11), 94.1),
        ((26, 1, 0), (26, 1, 2), 101.1),
    ]

    def parse_version(v: str) -> tuple:
        parts = v.strip().split(".")
        # Pad to 3 parts: "1.21" -> (1, 21, 0)
        while len(parts) < 3:
            parts.append("0")
        return tuple(int(p) for p in parts)

    formats = RESOURCE_PACK_FORMATS if pack_type == "resource" else DATA_PACK_FORMATS

    try:
        v = parse_version(version)
    except ValueError:
        raise ValueError(f"Invalid version string: '{version}'")

    for min_v, max_v, fmt in formats:
        if min_v <= v <= max_v:
            return fmt

    return None  # version isn't found / not supported