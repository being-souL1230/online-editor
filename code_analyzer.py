from bs4 import BeautifulSoup
from bs4.element import Tag
from difflib import SequenceMatcher
import os

def smart_merge(old_code: str, updated_snippet: str):
    try:
        old_soup = BeautifulSoup(old_code, 'html.parser')
        update_soup = BeautifulSoup(updated_snippet, 'html.parser')
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return old_code, 0

    changes = 0
    for new_tag in update_soup.find_all():
        if not isinstance(new_tag, Tag):
            continue
        matching_old_tags = [t for t in old_soup.find_all() if isinstance(t, Tag) and t.name == new_tag.name]

        best_match = None
        highest_ratio = 0

        for old_tag in matching_old_tags:
            ratio = SequenceMatcher(None, str(old_tag), str(new_tag)).ratio()
            if ratio > highest_ratio:
                best_match = old_tag
                highest_ratio = ratio

        if highest_ratio < 0.8:
            if old_soup.body:
                old_soup.body.append(new_tag)
            else:
                old_soup.append(new_tag)
            changes += 1
        elif best_match:
            best_match.replace_with(new_tag)
            changes += 1

    return str(old_soup), changes

def read_multiline_input(prompt):
    print(prompt)
    print("(Paste code below. Press Enter on a blank line to finish.)")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)

def main():
    print("\n==== HTML Code Merger Tool ====")
    print("Choose input mode:")
    print("1. File Input (old.html + updated.html)")
    print("2. Paste Code Manually")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        try:
            with open("old.html", "r", encoding="utf-8") as f1:
                old_code = f1.read()
            with open("updated.html", "r", encoding="utf-8") as f2:
                updated_code = f2.read()
        except FileNotFoundError:
            print("\n❌ File not found. Please ensure 'old.html' and 'updated.html' exist.")
            return
    elif choice == "2":
        old_code = read_multiline_input("\n==== Enter OLD HTML CODE ====")
        updated_code = read_multiline_input("\n==== Enter UPDATED SNIPPET ====")
    else:
        print("\n❌ Invalid choice. Exiting.")
        return

    if not old_code.strip() or not updated_code.strip():
        print("\n❌ One or both code inputs are empty. Exiting.")
        return

    merged_code, changes = smart_merge(old_code, updated_code)

    if choice == "1":
        try:
            with open("merged_output.html", "w", encoding="utf-8") as f3:
                f3.write(merged_code)
            print(f"\n[✓] Merge complete. {changes} changes applied.")
            print("[✓] Output saved to 'merged_output.html'")
        except Exception as e:
            print(f"\n❌ Error writing output file: {e}")
    else:
        print("\n==== Merged Code Output ====")
        print(merged_code)
        print(f"\n[✓] Total Changes Applied: {changes}")

if __name__ == "__main__":
    main()