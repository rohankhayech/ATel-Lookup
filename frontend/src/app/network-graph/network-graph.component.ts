import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  Output,
} from '@angular/core';
import * as d3 from 'd3';
import {
  D3DragEvent,
  Selection,
  Simulation,
  SimulationLinkDatum,
  SimulationNodeDatum,
} from 'd3';

export interface Node extends SimulationNodeDatum {
  id: string;
}

export interface Link extends SimulationLinkDatum<Node> {}

interface DragEvent extends D3DragEvent<SVGCircleElement, Node, Node> {}

@Component({
  selector: 'app-network-graph',
  templateUrl: './network-graph.component.html',
  styleUrls: ['./network-graph.component.scss'],
})
export class NetworkGraphComponent implements OnChanges {
  @Output() public selectionChange = new EventEmitter<number>();

  @Input() public nodes: Node[] = [];
  @Input() public links: Link[] = [];

  private svg?: Selection<SVGSVGElement, unknown, HTMLElement, any>;

  constructor() {}

  ngOnChanges() {
    this.generate();
  }

  generate() {
    this.clear();

    this.svg = d3
      .select('#network-graph')
      .append('svg')
      .attr('width', '100%')
      .attr('height', '100%');

    const rect = this.svg.node()!.getBoundingClientRect();
    const width = rect?.width;
    const height = rect?.height;

    const simulation = d3
      .forceSimulation<Node>(this.nodes)
      .force(
        'link',
        d3.forceLink<Node, Link>(this.links).id((d) => d.id)
      )
      .force('charge', d3.forceManyBody())
      .force('center', d3.forceCenter(width / 2, height / 2));

    const link = this.svg
      .append('g')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6)
      .selectAll('line')
      .data(this.links)
      .join('line')
      .attr('stroke-width', 1);

    const node = this.svg
      .append('g')
      .attr('stroke', '#fff')
      .attr('stroke-width', 1.5)
      .selectAll('circle')
      .data(this.nodes)
      .join('circle')
      .attr('r', 5)
      .on('click', this.click.bind(this))
      .call((simulation: any) => this.drag(simulation));

    node.append('title').text((d) => d.id);

    simulation.on('tick', () => {
      link
        .attr('x1', (d) => (d.source as Node).x!)
        .attr('y1', (d) => (d.source as Node).y!)
        .attr('x2', (d) => (d.target as Node).x!)
        .attr('y2', (d) => (d.target as Node).y!);

      node.attr('cx', (d) => d.x!).attr('cy', (d) => d.y!);
    });
  }

  drag(simulation: Simulation<Node, Link>) {
    const dragStarted = (event: DragEvent) => {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    };

    const dragged = (event: DragEvent) => {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    };

    const dragEnded = (event: DragEvent) => {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    };

    return d3
      .drag<SVGCircleElement, Node>()
      .on('start', dragStarted)
      .on('drag', dragged)
      .on('end', dragEnded);
  }

  clear() {
    this.svg?.remove();
  }

  click(_: unknown, node: Node) {
    this.selectionChange.emit(+node.id);
  }
}
