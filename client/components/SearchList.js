import fetching from "../utilities/fetching.js";

export default class SearchList extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("search-list");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add("w-100");

    const search_input = this.querySelector(".search-input");
    const search_btn = this.querySelector(".search-btn");
    const search_results = this.querySelector(".search-results");

    search_btn.addEventListener("click", () => {
      search_results.innerHTML = "";
      fetching(
        `https://${window.ft_transcendence_host}/player/?username=${search_input.value}`,
      ).then((req) => {
        const arr = req.players;
        if (!arr || arr.length === 0) {
          const no_results = document.createElement("div");
          no_results.classList.add("text-center", "text-muted");
          no_results.textContent = "No results found";
          search_results.appendChild(no_results);
          return;
        }
        for (let i = 0; i < arr.length; i++) {
          const player_card_elem = document.createElement("friend-card");
          player_card_elem.setAttribute("friend-card-type", "search");
          player_card_elem.setAttribute("player-id", arr[i].id);
          player_card_elem.setAttribute("avatar", arr[i].avatar);
          player_card_elem.setAttribute("username", arr[i].username);
          search_results.appendChild(player_card_elem);
        }
      });
    });
  }
}

customElements.define("search-list", SearchList);
