// Collapsible tree based on https://observablehq.com/@d3/collapsible-tree by Mike Bostock
console.log(data);

const width = 1250;
const marginTop = 100;
const marginRight = 100;
const marginBottom = 100;
const marginLeft = 200;

const root = d3.hierarchy(data);
const dx = 60;
const dy = (width - marginRight - marginLeft) / (1 + root.height);

const tree = d3.tree().nodeSize([dx, dy]);
const diagonal = d3.linkHorizontal().x(d => d.y).y(d => d.x);

const svg = d3.create("svg")
  .attr("width", width)
  .attr("height", dy)
  .attr("viewBox", [-marginLeft, -marginTop, width, dy])
  .attr("style", "max-width: 100%; height: auto; font: 18px sans-serif; user-select: none;");

const gLink = svg.append("g")
  .attr("fill", "none")
  .attr("stroke", "#008000")
  .attr("stroke-opacity", 0.4)
  .attr("stroke-width", 1.5);

const gNode = svg.append("g")
  .attr("cursor", "pointer")
  .attr("pointer-events", "all");

function update(event, source) {
  const duration = event?.altKey ? 2500 : 250;
  const nodes = root.descendants().reverse();
  const links = root.links();

  tree(root);

  let left = root;
  let right = root;
  root.eachBefore(node => {
    if (node.x < left.x) left = node;
    if (node.x > right.x) right = node;
  });

  const height = right.x - left.x + marginTop + marginBottom;

  const transition = svg.transition()
    .duration(duration)
    .attr("height", height)
    .attr("viewBox", [-marginLeft, left.x - marginTop, width, height])
    .tween("resize", window.ResizeObserver ? null : () => () => svg.dispatch("toggle"));

  const node = gNode.selectAll("g")
    .data(nodes, d => d.id);

  const nodeEnter = node.enter().append("g")
    .attr("transform", d => `translate(${source.y0},${source.x0})`)
    .attr("fill-opacity", 0)
    .attr("stroke-opacity", 0)
    .on("click", (event, d) => {
      d.children = d.children ? null : d._children;
      update(event, d);
    });

  nodeEnter.append("circle")
    .attr("r", 4)
    .attr("fill", d => d._children ? "#555" : "#999")
    .attr("stroke-width", 10);

  nodeEnter.append("text")
    .attr("dy", "0.31em")
    .attr("x", d => d._children ? -6 : 6)
    .attr("text-anchor", d => d._children ? "end" : "start")
    .each(function (d) {
      if (d.data.name.match(/\((.*?)\)/)?.[1]) {
        d3.select(this).append("a")
          .attr("href", d => {
            return "pcwkb_core/species_page/" + d.data.name.match(/\((.*?)\)/)?.[1];
          })
          .text(d => d.data.name)
          .attr("fill", "green")
          .attr("stroke-linejoin", "round")
          .attr("stroke-width", 3)
          .attr("stroke", "white")
          .attr("paint-order", "stroke")
          .attr("font-style", "italic");
      }
      else {
        d3.select(this).append("tspan")
          .text(d => d.data.name)
          .attr("stroke-linejoin", "round")
          .attr("stroke-width", 6)
          .attr("stroke", "white")
          .attr("paint-order", "stroke");
      }
    });

  const nodeUpdate = node.merge(nodeEnter).transition(transition)
    .attr("transform", d => `translate(${d.y},${d.x})`)
    .attr("fill-opacity", 1)
    .attr("stroke-opacity", 1);

  const nodeExit = node.exit().transition(transition).remove()
    .attr("transform", d => `translate(${source.y},${source.x})`)
    .attr("fill-opacity", 0)
    .attr("stroke-opacity", 0);

  const link = gLink.selectAll("path")
    .data(links, d => d.target.id);

  const linkEnter = link.enter().append("path")
    .attr("d", d => {
      const o = { x: source.x0, y: source.y0 };
      return diagonal({ source: o, target: o });
    });

  link.merge(linkEnter).transition(transition)
    .attr("d", diagonal);

  link.exit().transition(transition).remove()
    .attr("d", d => {
      const o = { x: source.x, y: source.y };
      return diagonal({ source: o, target: o });
    });

  root.eachBefore(d => {
    d.x0 = d.x;
    d.y0 = d.y;
  });
}

root.x0 = dy / 2;
root.y0 = 0;
root.descendants().forEach((d, i) => {
  d.id = i;
  d._children = d.children;
  if (d !== root) d.children = null;
});

update(null, root);

var div = document.getElementById('species_tree');

div.appendChild(svg.node());