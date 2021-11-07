'use strict';

import misspells from './spells/misspells.js';

const cast = document.getElementById('cast');
const misstainer = document.getElementById('misstainer');
const misspell = document.getElementById('misspell');

const randomChoice = arr => arr[Math.floor(Math.random() * arr.length)];

const fadeTransition = (div, newValue) => {
  div.classList.add('hidden');
  setTimeout(() => {
    div.textContent = newValue;
    div.classList.remove('hidden');
  }, 200);
};

cast.addEventListener('click', function () {
  misstainer.classList.remove('hidden');
  fadeTransition(misspell, randomChoice(misspells));
});
