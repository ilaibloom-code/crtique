// ═══════════════════════════════════════
// ÉTOILES
// ═══════════════════════════════════════

const stars = document.querySelectorAll('.star');
let noteChoisie = 0; // note sélectionnée (0 = rien)
let aVote = false; // a-t-on déjà voté dans cette session ?

// Allume les N premières étoiles
function setActive(n) {
    stars.forEach((s, i) => s.classList.toggle('active', i < n));
}

stars.forEach(s => {
    // Survol : prévisualise
    s.addEventListener('mouseenter', () => {
        if (aVote) return;
        setActive(+s.dataset.n);
        s.classList.add('hover');
    });

    // Fin de survol : revient à la sélection en cours
    s.addEventListener('mouseleave', () => {
        if (aVote) return;
        setActive(noteChoisie); // reste sur la note choisie (pas 0)
        s.classList.remove('hover');
    });

    // Clic : sélectionne la note
    s.addEventListener('click', () => {
        if (aVote) return;
        noteChoisie = +s.dataset.n;
        setActive(noteChoisie);
        document.getElementById('msg-vote').textContent =
            `Vous avez choisi ${noteChoisie} étoile${noteChoisie > 1 ? 's' : ''}. Remplissez le formulaire puis envoyez !`;
    });
});

// ═══════════════════════════════════════
// ENVOI DU FORMULAIRE
// ═══════════════════════════════════════

function envoyerFormulaire() {
    if (aVote) return;

    if (noteChoisie === 0) {
        afficherMsg('Choisissez d\'abord une note avec les étoiles.', 'erreur');
        return;
    }

    const prenom = document.getElementById('prenom').value.trim();
    const commentaire = document.getElementById('commentaire').value.trim();

    // On envoie tout au serveur Flask en JSON
    // Flask lit ça avec : request.json.get("note") etc.
    fetch('/vote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            note: noteChoisie,
            prenom: prenom,
            commentaire: commentaire
        })
    })
    .then(r => r.json())
    // .then() s'exécute quand le serveur répond
    // r => r.json() transforme la réponse HTTP en objet JavaScript
    .then(data => {
        if (data.erreur) {
            afficherMsg(data.erreur, 'erreur');
        } else {
            aVote = true;
            document.getElementById('btn-envoyer').disabled = true;
            stars.forEach(s => s.style.cursor = 'default');
            afficherMsg(
                `Merci ${prenom || 'Anonyme'} ! Moyenne actuelle : ${data.moyenne}/5 (${data.nb_votes} votes)`,
                'succes'
            );
            // Mettre à jour les résultats
            mettreAJourResultats();
        }
    });
}

function afficherMsg(msg, type) {
    const p = document.getElementById('msg-vote');
    p.textContent = msg;
    p.className = type;
}

function mettreAJourResultats() {
    fetch('/resultats')
    .then(r => r.json())
    .then(data => {
        document.querySelector('#resultats p').textContent = `Moyenne actuelle: ${data.moyenne}/5 (${data.nb_votes} votes)`;
        const ul = document.querySelector('#resultats ul');
        ul.innerHTML = '';
        data.historique.forEach(vote => {
            const li = document.createElement('li');
            li.textContent = `Note: ${vote.note}, Prénom: ${vote.prenom}, Commentaire: ${vote.commentaire}, Moyenne: ${vote.moyenne}`;
            ul.appendChild(li);
        });
    });
}