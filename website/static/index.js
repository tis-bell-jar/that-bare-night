function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const notesList = document.getElementById("notes");
  if (notesList) {
    new Sortable(notesList, {
      animation: 150,
      onEnd: () => {
        const order = Array.from(notesList.children).map((li) => li.dataset.id);
        fetch("/reorder-notes", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ order: order }),
        });
      },
    });
  }
});
