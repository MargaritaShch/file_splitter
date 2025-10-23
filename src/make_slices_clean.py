# src/make_slices_clean.py
from __future__ import annotations
from pathlib import Path
import argparse
import itertools


def values_stream(path: Path):
    """Построчно отдаёт очищенные значения из файла, пропуская хедер."""
    with path.open("r", encoding="utf-8-sig", errors="replace") as f:
        # пропускаем первую строку (заголовок)
        next(f, None)
        for line in f:
            v = line.strip().strip('"').strip("'")
            if v:
                yield v


def write_n(it, out_path: Path, n: int) -> int:
    """Записывает не более n значений из итератора. Возвращает количество записанных строк."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cnt = 0
    with out_path.open("w", encoding="utf-8", newline="") as out:
        for v in itertools.islice(it, n):
            out.write(v + "\n")
            cnt += 1
    return cnt


def skip_n(it, n: int) -> int:
    """Пропускает n элементов. Возвращает сколько реально пропустили."""
    return sum(1 for _ in itertools.islice(it, n))


def slice_csv(src_path: Path, out_dir: Path, prefix: str,
              n_read: int, n_write: int, n_delete: int,
              delete_mark: int = 1_500_000):
    """Формирует read/write/delete-срезы из одного CSV."""
    it = values_stream(src_path)

    # read
    read_path = out_dir / f"{prefix}_read_{n_read}.csv"
    c_read = write_n(it, read_path, n_read)

    # write
    write_path = out_dir / f"{prefix}_write_{n_write}.csv"
    c_write = write_n(it, write_path, n_write)

    # delete
    already = c_read + c_write
    need_skip = max(0, delete_mark - already)
    skip_n(it, need_skip)
    delete_path = out_dir / f"{prefix}_delete_{n_delete}.csv"
    c_delete = write_n(it, delete_path, n_delete)

    print(f"[{prefix}] read={c_read}, write={c_write}, delete={c_delete}")


def main():
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description="Разрез CSV на read/write/delete-срезы")
    p.add_argument("--x5id", default=str(base / "x5id_for_nt.csv"))
    p.add_argument("--mobile", default=str(base / "mobile_for_nt.csv"))
    p.add_argument("--outdir", default=str(base / "files" / "data_slices"))
    p.add_argument("--n-read", type=int, default=500_000)
    p.add_argument("--n-write", type=int, default=1_000_000)
    p.add_argument("--n-delete", type=int, default=30_000)
    p.add_argument("--delete-mark", type=int, default=1_500_000)
    args = p.parse_args()

    out_dir = Path(args.outdir)

    slice_csv(Path(args.x5id), out_dir, "x5id",
              args.n_read, args.n_write, args.n_delete, args.delete_mark)
    slice_csv(Path(args.mobile), out_dir, "mobile",
              args.n_read, args.n_write, args.n_delete, args.delete_mark)

    print(f"Direction: {out_dir}")


if __name__ == "__main__":
    main()
