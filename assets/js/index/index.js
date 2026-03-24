/**
 * index.js — TerminalSouls
 * Handles all UI logic: setup flow, animation, turn management, and pywebview bridge.
 */

"use strict";

function waitForApi(cb) {
    console.log('[TS] waitForApi tick — pywebview:', !!window.pywebview, '| api:', !!(window.pywebview && window.pywebview.api), '| init_game:', !!(window.pywebview && window.pywebview.api && window.pywebview.api.init_game));
    if (window.pywebview && window.pywebview.api && window.pywebview.api.init_game) {
        console.log('[TS] API ready, calling main()');
        cb();
    } else {
        setTimeout(() => waitForApi(cb), 50);
    }
}

waitForApi(main);

function main() {

// ============================================================
// CONSTANTS
// ============================================================

const ASSETS = "../../assets/images/ui";

const ANIM_FRAMES = {
    hero:  { Dying: 15, Hurt: 12, Idle: 18, "Idle Blinking": 18, Slashing: 12, Sliding: 6 },
    enemy: { Dying: 15, Hurt: 12, Idle: 18, "Idle Blinking": 18, Slashing: 12, Sliding: 6 }
};

const ANIM_FPS = 10;

const HERO_CARDS = [
    { icon: "runeSkillSword.png",   label: "Attack",        folder: "hero" },
    { icon: "runeSkillHealth.png",  label: "Use Potion",    folder: "hero" },
    { icon: "runeSkillSpecial.png", label: "Special Skill", folder: "hero" }
];

const ENEMY_CARDS = [
    { icon: "runeSkillSwordMalevus.png",  label: "???", folder: "enemy" },
    { icon: "runeSkillHealthMalevus.png", label: "???", folder: "enemy" },
    { icon: "runeNotSkill.png",           label: "???", folder: "enemy" }
];

const BACKGROUNDS_COUNT = 4;

// ============================================================
// STATE
// ============================================================

const state = {
    heroName:      "",
    heroGender:    "",
    currentTurn:   "hero",
    turnNumber:    1,
    isAnimating:   false,
    rageActive:    false,
    heroMaxLife:   100,
    enemyMaxLife:  120,
    heroPotions:   3,
    gameActive:    false,
    animIntervals: { hero: null, enemy: null }
};

// ============================================================
// DOM REFS
// ============================================================

const dom = {
    screenSetup:     document.getElementById("screen-setup"),
    screenLoading:   document.getElementById("screen-loading"),
    screenGame:      document.getElementById("screen-game"),

    stepName:        document.getElementById("step-name"),
    stepGender:      document.getElementById("step-gender"),
    inputName:       document.getElementById("input-name"),
    nameError:       document.getElementById("name-error"),
    btnNameNext:     document.getElementById("btn-name-next"),

    loadingBg:       document.getElementById("loading-bg"),

    gameBg:          document.getElementById("game-bg"),
    heroNameLabel:   document.getElementById("hero-name-label"),
    enemyNameLabel:  document.getElementById("enemy-name-label"),
    heroLifeFill:    document.getElementById("hero-life-fill"),
    enemyLifeFill:   document.getElementById("enemy-life-fill"),
    heroLifeText:    document.getElementById("hero-life-text"),
    enemyLifeText:   document.getElementById("enemy-life-text"),
    potionsRow:      document.getElementById("potions-row"),
    turnBadge:       document.getElementById("turn-badge"),
    turnNumber:      document.getElementById("turn-number"),

    heroFrame:       document.getElementById("hero-frame"),
    enemyFrame:      document.getElementById("enemy-frame"),
    heroSprite:      document.getElementById("hero-sprite"),
    enemySprite:     document.getElementById("enemy-sprite"),
    rageAura:        document.getElementById("rage-aura"),

    cards:     [
        document.getElementById("card-1"),
        document.getElementById("card-2"),
        document.getElementById("card-3"),
        document.getElementById("card-4")
    ],
    cardIcons: [
        document.getElementById("card-icon-1"),
        document.getElementById("card-icon-2"),
        document.getElementById("card-icon-3")
    ],
    cardLabels: [
        document.getElementById("card-label-1"),
        document.getElementById("card-label-2"),
        document.getElementById("card-label-3")
    ],
    rageBorders: [
        document.getElementById("rage-border-1"),
        document.getElementById("rage-border-3")
    ],

    logMessages:     document.getElementById("log-messages"),
    logArea:         document.getElementById("log-area"),

    gameOverOverlay: document.getElementById("game-over-overlay"),
    gameOverTitle:   document.getElementById("game-over-title"),
    gameOverSub:     document.getElementById("game-over-subtitle"),
    btnRestart:      document.getElementById("btn-restart"),

    potionFloat:    document.getElementById("potion-float"),
    potionFloatImg: document.getElementById("potion-float-img")
};

// ============================================================
// SETUP FLOW
// ============================================================

function validateName(value) {
    const trimmed = value.trim();
    if (!trimmed) return "Name cannot be empty.";
    if (!/^[a-zA-Z\s]+$/.test(trimmed)) return "Name must contain letters only.";
    if (trimmed.length > 20) return "Name cannot exceed 20 characters.";
    return null;
}

dom.btnNameNext.addEventListener("click", () => {
    const error = validateName(dom.inputName.value);
    if (error) {
        dom.nameError.textContent = error;
        dom.nameError.classList.remove("hidden");
        return;
    }
    dom.nameError.classList.add("hidden");
    state.heroName = dom.inputName.value.trim();
    dom.stepName.classList.add("hidden");
    dom.stepGender.classList.remove("hidden");
});

dom.inputName.addEventListener("keydown", (e) => {
    if (e.key === "Enter") dom.btnNameNext.click();
});

document.querySelectorAll(".gender-card").forEach(card => {
    card.addEventListener("click", () => {
        state.heroGender = card.dataset.gender;
        startLoading();
    });
});

// ============================================================
// LOADING & TRANSITION
// ============================================================

function pickRandomBackground() {
    return Math.floor(Math.random() * BACKGROUNDS_COUNT) + 1;
}

function startLoading() {
    console.log("[TS] startLoading(), heroGender:", state.heroGender, "heroName:", state.heroName);
    const bgNum  = pickRandomBackground();
    const bgPath = `${ASSETS}/backgrounds/${bgNum}.png`;

    dom.loadingBg.style.backgroundImage = `url('${bgPath}')`;
    dom.gameBg.style.backgroundImage    = `url('${bgPath}')`;

    showScreen(dom.screenLoading);

    setTimeout(() => {
        initGame();
    }, 2200);
}

function showScreen(screen) {
    console.log("[TS] showScreen:", screen.id);
    [dom.screenSetup, dom.screenLoading, dom.screenGame].forEach(s => {
        s.classList.remove("active");
    });
    screen.classList.add("active");
}

// ============================================================
// GAME INIT
// ============================================================

async function initGame() {
    console.log("[TS] initGame() called, heroName:", state.heroName);
    console.log("[TS] calling pywebview.api.init_game with:", state.heroName);
    const result = await window.pywebview.api.init_game(state.heroName);
    console.log("[TS] init_game result:", result);
    const gs     = result.state;

    state.heroMaxLife  = gs.hero.max_life;
    state.enemyMaxLife = gs.enemy.max_life;
    state.heroPotions  = gs.hero.potions;
    state.gameActive   = true;
    state.turnNumber   = 1;
    state.currentTurn  = "hero";
    state.rageActive   = false;

    dom.heroNameLabel.textContent  = gs.hero.name;
    dom.enemyNameLabel.textContent = gs.enemy.name;

    updateHUD(gs);
    setHeroCards();
    startIdleAnimation("hero");
    startIdleAnimation("enemy");

    showScreen(dom.screenGame);
    setTurnUI("hero");
    enableCards(true);
    addLog(result.message, "system");
}

// ============================================================
// HUD UPDATE
// ============================================================

function updateHUD(gs) {
    const heroPct  = Math.max(0, (gs.hero.current_life  / state.heroMaxLife)  * 100);
    const enemyPct = Math.max(0, (gs.enemy.current_life / state.enemyMaxLife) * 100);

    dom.heroLifeFill.style.width  = `${heroPct}%`;
    dom.enemyLifeFill.style.width = `${enemyPct}%`;
    dom.heroLifeText.textContent  = `${gs.hero.current_life} / ${state.heroMaxLife}`;
    dom.enemyLifeText.textContent = `${gs.enemy.current_life} / ${state.enemyMaxLife}`;

    renderPotions(gs.hero.potions);
    state.heroPotions = gs.hero.potions;
}

function renderPotions(count) {
    dom.potionsRow.innerHTML = "";
    for (let i = 0; i < 3; i++) {
        const img     = document.createElement("img");
        img.className = "potion-icon";
        img.src       = i < count
            ? `${ASSETS}/items/fullPotion.png`
            : `${ASSETS}/items/emptyPotion.png`;
        img.alt = i < count ? "potion" : "empty";
        dom.potionsRow.appendChild(img);
    }
}

// ============================================================
// CARDS
// ============================================================

function setHeroCards() {
    HERO_CARDS.forEach((card, i) => {
        dom.cardIcons[i].src          = `${ASSETS}/skills/icons/${card.folder}/${card.icon}`;
        dom.cardLabels[i].textContent = card.label;
    });
    dom.cards[3].querySelector(".card-label").textContent = "Skip Turn";
}

function setEnemyCards() {
    ENEMY_CARDS.forEach((card, i) => {
        dom.cardIcons[i].src          = `${ASSETS}/skills/icons/${card.folder}/${card.icon}`;
        dom.cardLabels[i].textContent = card.label;
    });
    dom.cards[3].querySelector(".card-label").textContent = "???";
}

function enableCards(enabled) {
    dom.cards.forEach(card => {
        card.classList.toggle("disabled",     !enabled);
        card.classList.toggle("enemy-active", !enabled);
    });
}

function setRageUI(active) {
    state.rageActive = active;
    dom.rageAura.classList.toggle("hidden",  !active);
    dom.rageBorders[0].classList.toggle("hidden", !active);
    dom.rageBorders[1].classList.toggle("hidden", !active);
}

// ============================================================
// TURN UI
// ============================================================

function setTurnUI(who) {
    state.currentTurn = who;
    dom.turnNumber.textContent = state.turnNumber;

    if (who === "hero") {
        dom.turnBadge.textContent = "Your Turn";
        dom.turnBadge.classList.remove("enemy-turn");
        setHeroCards();
        enableCards(true);
    } else {
        dom.turnBadge.textContent = "Enemy Turn";
        dom.turnBadge.classList.add("enemy-turn");
        setEnemyCards();
        enableCards(false);
    }
}

// ============================================================
// CARD CLICK
// ============================================================

dom.cards.forEach(card => {
    card.addEventListener("click", () => {
        if (state.isAnimating || !state.gameActive) return;
        const option = parseInt(card.dataset.option, 10);
        handlePlayerAction(option);
    });
});

async function handlePlayerAction(option) {
    state.isAnimating = true;
    enableCards(false);

    await runHeroTurnAnimation(option);

    const result = await window.pywebview.api.process_turn(option);
    const gs     = result.state;
    const msgs   = result.message;

    updateHUD(gs);

    const isHeroDead  = gs.hero.current_life  <= 0;
    const isEnemyDead = gs.enemy.current_life <= 0;

    if (option === 1 || option === 3) {
        if (isEnemyDead) {
            await runAnimation("enemy", "Dying");
        } else {
            await runAnimation("enemy", "Hurt");
        }
        startIdleAnimation("enemy");
    }

    if (isEnemyDead || isHeroDead) {
        addLog(msgs, "new");
        endGame(isHeroDead);
        return;
    }

    const midpoint = Math.ceil(msgs.length / 2);
    addLog(msgs.slice(0, midpoint), "new");

    if (option === 2) {
        floatPotion("hero");
    }

    if (state.rageActive && (option === 1 || option === 3)) {
        setRageUI(false);
    }

    await delay(400);
    setTurnUI("enemy");
    await delay(800);

    await runEnemyTurnAnimation(msgs, gs);

    updateHUD(gs);

    if (gs.hero.current_life <= 0) {
        await runAnimation("hero", "Dying");
        addLog(msgs.slice(midpoint), "new");
        endGame(true);
        return;
    }

    addLog(msgs.slice(midpoint), "");

    const rageTriggered = msgs.some(m => m.toLowerCase().includes("rage"));
    if (rageTriggered) {
        setRageUI(true);
    }

    state.turnNumber++;
    state.isAnimating = false;
    setTurnUI("hero");
}

// ============================================================
// ANIMATIONS
// ============================================================

function spriteBasePath(who, anim) {
    if (who === "hero") {
        return `${ASSETS}/characters/hero/${state.heroGender}/${anim}/`;
    }
    return `${ASSETS}/characters/enemy/male/${anim}/`;
}

function frameCount(who, anim) {
    return ANIM_FRAMES[who][anim] || 8;
}

function runAnimation(who, anim) {
    return new Promise(resolve => {
        const img      = who === "hero" ? dom.heroFrame : dom.enemyFrame;
        const basePath = spriteBasePath(who, anim);
        const total    = frameCount(who, anim);
        let frame      = 0;

        clearInterval(state.animIntervals[who]);

        state.animIntervals[who] = setInterval(() => {
            img.src = `${basePath}${frame}.png`;
            frame++;
            if (frame >= total) {
                clearInterval(state.animIntervals[who]);
                resolve();
            }
        }, 1000 / ANIM_FPS);
    });
}

function startIdleAnimation(who) {
    const img      = who === "hero" ? dom.heroFrame : dom.enemyFrame;
    const basePath = spriteBasePath(who, "Idle");
    const total    = frameCount(who, "Idle");
    let frame      = 0;

    clearInterval(state.animIntervals[who]);

    state.animIntervals[who] = setInterval(() => {
        img.src = `${basePath}${frame}.png`;
        frame   = (frame + 1) % total;
    }, 1000 / ANIM_FPS);
}

async function runHeroTurnAnimation(option) {
    if (option === 1 || option === 3) {
        dom.heroSprite.classList.add("hero-charging");
        await delay(400);
        await runAnimation("hero", "Slashing");
        dom.heroSprite.classList.remove("hero-charging");
    }
    startIdleAnimation("hero");
}

async function runEnemyTurnAnimation(msgs, gs) {
    const heroSlid   = msgs.some(m => m.toLowerCase().includes("dodge") && m.toLowerCase().includes("hero"));
    const enemyHeals = msgs.some(m => m.toLowerCase().includes("enemy manages to heal"));

    if (enemyHeals) {
        floatPotion("enemy");
        await delay(800);
    }

    dom.enemySprite.classList.add("enemy-charging");
    await delay(400);
    await runAnimation("enemy", "Slashing");
    dom.enemySprite.classList.remove("enemy-charging");

    if (heroSlid) {
        await runAnimation("hero", "Sliding");
    } else {
        await runAnimation("hero", "Hurt");
    }

    startIdleAnimation("hero");
    startIdleAnimation("enemy");
}

// ============================================================
// POTION FLOAT
// ============================================================

function floatPotion(who) {
    const slotId = who === "hero" ? "hero-slot" : "enemy-slot";
    const rect   = document.getElementById(slotId).getBoundingClientRect();

    dom.potionFloatImg.src          = `${ASSETS}/items/fullPotion.png`;
    dom.potionFloat.style.left      = `${rect.left + rect.width / 2 - 20}px`;
    dom.potionFloat.style.top       = `${rect.top + 40}px`;
    dom.potionFloat.style.opacity   = "1";
    dom.potionFloat.style.transform = "translateY(0)";
    dom.potionFloat.classList.remove("hidden");

    setTimeout(() => {
        dom.potionFloat.style.transform = "translateY(-60px)";
        dom.potionFloat.style.opacity   = "0";
    }, 50);

    setTimeout(() => {
        dom.potionFloat.classList.add("hidden");
        dom.potionFloat.style.transform = "translateY(0)";
    }, 900);
}

// ============================================================
// LOG
// ============================================================

function addLog(messages, cls) {
    if (!messages || !messages.length) return;
    messages.forEach(msg => {
        const el       = document.createElement("div");
        el.className   = `log-entry${cls ? " " + cls : ""}`;
        el.textContent = msg;
        dom.logMessages.prepend(el);

        if (cls === "new") {
            setTimeout(() => el.classList.remove("new"), 2000);
        }
    });
    dom.logArea.scrollTop = 0;
}

// ============================================================
// GAME OVER
// ============================================================

function endGame(heroLost) {
    state.gameActive  = false;
    state.isAnimating = false;
    clearInterval(state.animIntervals.hero);
    clearInterval(state.animIntervals.enemy);

    dom.gameOverTitle.textContent = heroLost ? "Defeated" : "Victory";
    dom.gameOverSub.textContent   = heroLost
        ? "The darkness has claimed another soul. Rise again, warrior."
        : "You have vanquished the enemy. The realm is safe... for now.";

    dom.gameOverOverlay.classList.remove("hidden");
}

dom.btnRestart.addEventListener("click", () => {
    dom.gameOverOverlay.classList.add("hidden");
    dom.logMessages.innerHTML = "";
    dom.inputName.value       = "";
    dom.nameError.classList.add("hidden");
    dom.stepGender.classList.add("hidden");
    dom.stepName.classList.remove("hidden");
    setRageUI(false);
    showScreen(dom.screenSetup);
});

// ============================================================
// UTILS
// ============================================================

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

}