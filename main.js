// import Matchup from './Matchup.js';

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

fetch('matchup_data.json')
    .then((response) => response.text())
    .then((text) => {
        let ms = [];
        const json = JSON.parse(text);
        for (let i = 0; i < 63; i++) {
            const matchup = json.mens[i];
            const {winner, team1, team2} = matchup;
            ms.push(new Matchup(ctx, i, winner, team1, team2));
        }
    });
