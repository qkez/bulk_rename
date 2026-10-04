import argparse
import re
from pathlib import Path


def rename_files(
    directory: Path,
    pattern: str | None = None,
    prefix: str | None = None,
    start: int = 1,
    padding: int = 3,
    uppercase: bool = False,
    lowercase: bool = False,
    dry_run: bool = True,
):
    if not directory.exists():
        print(f"Папка не найдена: {directory}")
        return

    if not directory.is_dir():
        print(f"Это не папка: {directory}")
        return

    files = sorted([f for f in directory.iterdir() if f.is_file()])
    if not files:
        print("Файлов нет.")
        return

    counter = start
    renamed = 0

    for file in files:
        new_name = file.name


        if pattern:
            try:
                new_name = re.sub(pattern, "", new_name)
            except re.error as e:
                print(f"Ошибка в регулярке: {e}")
                return


        if uppercase:
            new_name = new_name.upper()
        elif lowercase:
            new_name = new_name.lower()


        if prefix:
            suffix = file.suffix
            new_name = f"{prefix}_{str(counter).zfill(padding)}{suffix}"
            counter += 1


        if new_name == file.name:
            continue

        new_path = directory / new_name


        if new_path.exists():
            print(f"⚠ Пропуск {file.name} — {new_name} уже существует")
            continue

        if dry_run:
            print(f"[DRY] {file.name} -> {new_name}")
        else:
            file.rename(new_path)
            print(f"{file.name} -> {new_name}")
            renamed += 1

    if dry_run:
        print("\n[DRY RUN] Ничего не изменено. Убери --no-dry, чтобы применить.")
    else:
        print(f"\nГотово! Переименовано: {renamed}")


def main():
    parser = argparse.ArgumentParser(
        description="Массовое переименование файлов в папке"
    )
    parser.add_argument("directory", help="Путь к папке с файлами")
    parser.add_argument("--prefix", help="Префикс для имён (напр. vacation_2024)")
    parser.add_argument("--pattern", help="Regex — что удалить из имени")
    parser.add_argument("--start", type=int, default=1, help="Начальный номер")
    parser.add_argument("--padding", type=int, default=3, help="Сколько нулей")
    parser.add_argument("--uppercase", action="store_true", help="В ВЕРХНИЙ РЕГИСТР")
    parser.add_argument("--lowercase", action="store_true", help="в нижний регистр")
    parser.add_argument(
        "--no-dry",
        action="store_false",
        dest="dry_run",
        help="Выполнить реально (по умолчанию dry-run)",
    )

    args = parser.parse_args()

    rename_files(
        directory=Path(args.directory),
        pattern=args.pattern,
        prefix=args.prefix,
        start=args.start,
        padding=args.padding,
        uppercase=args.uppercase,
        lowercase=args.lowercase,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()