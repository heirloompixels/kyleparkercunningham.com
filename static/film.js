// Click-to-load film players. Each .film-facade holds a link to the film; on
// click it is replaced by the embedded player, so nothing is fetched from
// YouTube or Vimeo until a visitor asks for the film.
document.addEventListener("click", function (event) {
  var link = event.target.closest(".film-facade .film-play");
  if (!link) return;
  var figure = link.closest(".film-facade");
  var src = figure.getAttribute("data-src");
  if (!src) return;
  event.preventDefault();
  var frame = document.createElement("iframe");
  frame.src = src;
  frame.title = figure.getAttribute("data-title") || "Film";
  frame.allow = "autoplay; fullscreen; picture-in-picture; encrypted-media";
  frame.allowFullscreen = true;
  figure.replaceChildren(frame);
  figure.classList.remove("film-facade");
  frame.focus();
});
