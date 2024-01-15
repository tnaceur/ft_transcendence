// Router
import router from "./router/router.js";

// Components
import Navbar from "./components/Navbar.js";
import PlayCard from "./components/PlayCard.js";
import FriendCard from "./components/FriendCard.js";
import MatchCard from "./components/MatchCard.js";

// Pages
import GamePage from "./pages/GamePage.js";
import HomePage from "./pages/HomePage.js";
import LoginPage from "./pages/LoginPage.js";
import ProfilePage from "./pages/ProfilePage.js";
import SettingPage from "./pages/SettingPage.js";
import TournamentPage from "./pages/TournamentPage.js";
import NotfoundPage from "./pages/NotfoundPage.js";

window.addEventListener("DOMContentLoaded", () => {
  router.init();
});
