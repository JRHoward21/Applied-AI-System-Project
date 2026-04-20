const games = [
  {
    title: "Elden Ring",
    genres: ["RPG", "Action", "Adventure"],
    platforms: ["PC", "PlayStation 5", "Xbox Series X"],
    tags: ["open world", "combat", "exploration", "fantasy", "challenging"],
    reason: "Because you seem to like open-world action, exploration, and strong progression."
  },
  {
    title: "Alan Wake 2",
    genres: ["Horror", "Adventure"],
    platforms: ["PC", "PlayStation 5", "Xbox Series X"],
    tags: ["story", "horror", "mystery", "cinematic", "atmosphere"],
    reason: "A strong match for story-rich horror and cinematic gameplay."
  },
  {
    title: "Hades",
    genres: ["Action", "Indie"],
    platforms: ["PC", "Nintendo Switch", "PlayStation 5", "Xbox Series X"],
    tags: ["fast-paced", "combat", "replayable", "stylish", "roguelike"],
    reason: "Great if you enjoy fast action, replayability, and stylish combat."
  },
  {
    title: "Persona 5 Royal",
    genres: ["RPG"],
    platforms: ["PC", "Nintendo Switch", "PlayStation 5", "Xbox Series X"],
    tags: ["story", "turn-based", "style", "characters", "anime"],
    reason: "Recommended for narrative-heavy RPG fans who like strong characters and style."
  },
  {
    title: "The Last of Us Part II",
    genres: ["Action", "Adventure", "Horror"],
    platforms: ["PlayStation 5"],
    tags: ["story", "cinematic", "survival", "emotional", "stealth"],
    reason: "A great fit if you like emotional stories, survival tension, and polished gameplay."
  },
  {
    title: "Cyberpunk 2077",
    genres: ["RPG", "Action"],
    platforms: ["PC", "PlayStation 5", "Xbox Series X"],
    tags: ["open world", "story", "futuristic", "combat", "exploration"],
    reason: "A strong match for players who enjoy futuristic RPGs and open-world immersion."
  },
  {
    title: "Red Dead Redemption 2",
  genres: ["Action", "Adventure"],
  platforms: ["PC", "PlayStation 5", "Xbox Series X"],
  tags: ["open world", "story", "exploration", "western", "immersive"],
  reason: "A great fit for players who enjoy immersive worlds and strong storytelling."
},
{
  title: "Resident Evil 4",
  genres: ["Horror", "Action"],
  platforms: ["PC", "PlayStation 5", "Xbox Series X"],
  tags: ["survival", "horror", "combat", "tense", "story"],
  reason: "Perfect for players who like action-heavy survival horror."
},
{
  title: "Stardew Valley",
  genres: ["Indie", "Adventure"],
  platforms: ["PC", "Nintendo Switch", "PlayStation 5", "Xbox Series X"],
  tags: ["relaxing", "farming", "casual", "pixel", "cozy"],
  reason: "A strong recommendation if you enjoy chill, replayable, and cozy games."
}
];

const generateBtn = document.getElementById("generateBtn");
const recommendationCards = document.getElementById("recommendationCards");

generateBtn.addEventListener("click", generateRecommendations);

function generateRecommendations() {
  const system = document.getElementById("system").value;
  const favoriteGame = document.getElementById("favoriteGame").value.toLowerCase().trim();
  const history = document.getElementById("history").value.toLowerCase().trim();

  const checkedGenres = Array.from(
    document.querySelectorAll('.checkbox-group input[type="checkbox"]:checked')
  ).map((checkbox) => checkbox.value);

  const historyWords = history.split(/[\s,.-]+/).filter(Boolean);

  const scoredGames = games.map((game) => {
    let score = 0;

    if (system && game.platforms.includes(system)) {
      score += 3;
    }

    checkedGenres.forEach((genre) => {
      if (game.genres.includes(genre)) {
        score += 2;
      }
    });

    if (favoriteGame && game.title.toLowerCase().includes(favoriteGame)) {
      score += 4;
    }

    historyWords.forEach((word) => {
      if (game.tags.some((tag) => tag.toLowerCase().includes(word))) {
        score += 1;
      }
    });

    return { ...game, score };

    alert("Recommendations updated!");
  });

  scoredGames.sort((a, b) => b.score - a.score);

  const topGames = scoredGames.slice(0, 4);

  console.log("Top Games:", topGames);
  alert("Recommendations updated!");

  displayRecommendations(topGames);
}

function displayRecommendations(recommendations) {
  recommendationCards.innerHTML = "";

  if (recommendations.length === 0) {
    recommendationCards.innerHTML = `
      <p style="color: #aaa; font-size: 16px;">
        No matching games found. Try changing your preferences.
      </p>
    `;
    return;
  }

  recommendations.forEach((game) => {
    const card = document.createElement("div");
    card.classList.add("card");

    card.innerHTML = `
      <div class="card-banner">
        <h4>${game.title}</h4>
      </div>
      <small><strong>Genres:</strong> ${game.genres.join(", ")}</small>
      <small><strong>Platforms:</strong> ${game.platforms.join(", ")}</small>
      <p>${game.reason}</p>
      <div class="card-buttons">
        <button>View Match</button>
        <button class="secondary-btn">Save</button>
      </div>
    `;

    recommendationCards.appendChild(card);
  });
}

recommendationCards.innerHTML = `
  <p style="color: #aaa; font-size: 16px;">
    Select your preferences and click <strong>Generate Recommendations</strong>.
  </p>
`;

// Load default recommendations when page opens
recommendationCards.innerHTML = `
  <p style="color: #aaa; font-size: 16px;">
    Select your preferences and click <strong>Generate Recommendations</strong>.
  </p>
`;