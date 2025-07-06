from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import os

def smart_merge(old_code: str, updated_snippet: str):
    old_soup = BeautifulSoup(old_code, 'html.parser')
    update_soup = BeautifulSoup(updated_snippet, 'html.parser')

    changes = 0
    for new_tag in update_soup.find_all():
        matching_old_tags = old_soup.find_all(new_tag.name)

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
        line = input()
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

    merged_code, changes = smart_merge(old_code, updated_code)

    if choice == "1":
        with open("merged_output.html", "w", encoding="utf-8") as f3:
            f3.write(merged_code)
        print(f"\n[✓] Merge complete. {changes} changes applied.")
        print("[✓] Output saved to 'merged_output.html'")
    else:
        print("\n==== Merged Code Output ====")
        print(merged_code)
        print(f"\n[✓] Total Changes Applied: {changes}")

if __name__ == "__main__":
    main()