function deleteNote(noteId) {
  fetch('/delete-note', {
    method: 'POST',
    body: JSON.stringify({ noteId }),
  }).then(() => {
    window.location.href = '/';
  });
}

