function toggleSection(section) {
    const arrow = section.querySelector(".arrow");
    const content = section.nextElementSibling;

    arrow.classList.toggle("open");
    content.classList.toggle("show");
  }