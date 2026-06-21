import flet as ft
import json
import os

FILE_NAME = "notes.json"

def load_notes():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)

def main(page: ft.Page):
    page.title = "Notes App"
    page.window_width = 700
    page.window_height = 650
    page.padding = 20
    page.scroll = "auto"

    notes = load_notes()

    title_input = ft.TextField(label="Note title", width=300)
    content_input = ft.TextField(
        label="Note content",
        multiline=True,
        min_lines=4,
        max_lines=8,
        width=500
    )
    search_input = ft.TextField(label="Search notes", width=300)
    notes_column = ft.Column(spacing=10)

    edit_index = {"value": None}

    def refresh_notes(filter_text=""):
        notes_column.controls.clear()
        filter_text = filter_text.strip().lower()

        for i, note in enumerate(notes):
            if filter_text:
                full_text = f"{note['title']} {note['content']}".lower()
                if filter_text not in full_text:
                    continue

            def edit_note(e, index=i):
                title_input.value = notes[index]["title"]
                content_input.value = notes[index]["content"]
                edit_index["value"] = index
                page.update()

            def delete_note(e, index=i):
                notes.pop(index)
                save_notes(notes)
                if edit_index["value"] == index:
                    title_input.value = ""
                    content_input.value = ""
                    edit_index["value"] = None
                refresh_notes(search_input.value)
                page.update()

            card = ft.Card(
                content=ft.Container(
                    padding=12,
                    content=ft.Column([
                        ft.Row([
                            ft.Text(note["title"], size=18, weight="bold", expand=True),
                            ft.IconButton(icon=ft.Icons.EDIT, tooltip="Edit", on_click=edit_note),
                            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Delete", on_click=delete_note),
                        ]),
                        ft.Text(note["content"]),
                    ])
                )
            )
            notes_column.controls.append(card)

    def clear_inputs():
        title_input.value = ""
        content_input.value = ""
        edit_index["value"] = None

    def add_or_update_note(e):
        title = title_input.value.strip()
        content = content_input.value.strip()

        if not title and not content:
            return

        note_data = {"title": title or "Untitled", "content": content}

        if edit_index["value"] is None:
            notes.append(note_data)
        else:
            notes[edit_index["value"]] = note_data

        save_notes(notes)
        clear_inputs()
        refresh_notes(search_input.value)
        page.update()

    def on_search_change(e):
        refresh_notes(search_input.value)
        page.update()

    refresh_notes()

    page.add(
        ft.Text("My Notes App", size=28, weight="bold"),
        ft.Row([search_input], alignment=ft.MainAxisAlignment.START),
        ft.Row([title_input]),
        content_input,
        ft.Row([
            ft.ElevatedButton("Save Note", on_click=add_or_update_note),
            ft.OutlinedButton("Clear", on_click=lambda e: (clear_inputs(), page.update()))
        ]),
        ft.Divider(),
        notes_column
    )

    search_input.on_change = on_search_change

ft.app(target=main)
