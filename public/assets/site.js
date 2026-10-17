(() => {
  const controls = document.querySelector('[data-research-tools]');
  if (controls) {
    controls.hidden = false;
    const buttons = [...controls.querySelectorAll('[data-filter]')];
    const search = controls.querySelector('input');
    const papers = [...document.querySelectorAll('[data-publication]')];
    const count = document.querySelector('[data-result-count]');
    const empty = document.querySelector('[data-no-results]');
    let selected = 'all';
    const update = () => {
      const query = search.value.trim().toLocaleLowerCase();
      let visible = 0;
      for (const paper of papers) {
        const categoryMatches = selected === 'all' || paper.dataset.category === selected;
        const textMatches = paper.textContent.toLocaleLowerCase().includes(query);
        paper.hidden = !(categoryMatches && textMatches);
        if (!paper.hidden) visible++;
      }
      count.hidden = selected === 'all' && !query;
      count.textContent = `${visible} ${visible === 1 ? 'publication' : 'publications'}`;
      empty.hidden = visible !== 0;
      for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.filter === selected));
    };
    buttons.forEach(button => button.addEventListener('click', () => { selected = button.dataset.filter; update(); }));
    search.addEventListener('input', update);
  }
  document.querySelector('[data-print]')?.addEventListener('click', () => window.print());
})();
