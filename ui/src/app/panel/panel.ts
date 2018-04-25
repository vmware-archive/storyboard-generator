// Copyright © 2017-2018 VMware, Inc. All Rights Reserved.
// SPDX-License-Identifier: BSD-2-Clause

import { Component, Input, OnChanges, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { StoryboardApi, Panel, Position, Layer } from '../api/storyboard.api';
import { ASSET_SERVER_URL } from '../api/index';

interface Offset {
  x: number;
  y: number;
}

interface Dimensions {
  width: number;
  height: number;
}

interface RenderDetails {
  image?: HTMLImageElement;
  text?: string;
  offset: Offset;
  dimensions: Dimensions;
}

// Offset / Dimension Constants
const DEFAULT_OFFSET: Offset = { x: 0, y: 0 };
const BACKGROUND_OFFSET: Offset = { x: 0, y: 0 };
const BACKGROUND_DIMESIONS: Dimensions = { width: 600, height: 400 };

const DEFAULT_TEXT_DIMENSIONS: Dimensions = { width: 270, height: 400 };
const TEXT_Y_OFFSET = 10;

// Mapping of positions to offsets
const offsets: Map<Position, Offset> = new Map<Position, Offset>();
offsets.set(Position.LEFT, { x: 0, y: 0 });
offsets.set(Position.CENTER, { x: 150, y: 0 });
offsets.set(Position.RIGHT, { x: 310, y: 0 });

/** flatMap implementation */
const flatMap = function(array, callback) {
  return [].concat.apply([], array.map(callback));
};

/**
 * Root level component for the Alerts page.
 */
@Component({
  selector: 'app-panel',
  templateUrl: './panel.html',
  styleUrls: ['./panel.scss']
})
export class PanelComponent implements OnChanges, AfterViewInit {

  @Input() public panel: Panel;

  @ViewChild('canvas') canvas: ElementRef;
  context: CanvasRenderingContext2D;

  public ngOnChanges(changes) {
    if (changes.panel) {
      this.render();
    }
  }

  public ngAfterViewInit() {
    this.context = (<HTMLCanvasElement>this.canvas.nativeElement).getContext('2d');
    this.render();
  }

  private calculateBubbleSize(text: string, maxWidth: number, lineHeight: number, leftMargin: number, topMargin: number) {
    // Based on desired maxWidth, figure out how many linewraps
    // Return the total text height and the length of the longest line
    // (may be less than max width if text breaks are imperfect)
    const ctx = this.context;
    const words = text.split(' ');
    let line = '';
    let textHeight = 0;
    let longestLine = 0;
    const maxTextWidth = maxWidth - 2 * leftMargin;

    for (let n = 0; n < words.length; n++) {
      const testLine = line + words[n] + ' ';
      const metrics = ctx.measureText(testLine);
      const testWidth = metrics.width;
      // console.log("Line " + n + " width: " + testWidth)
      if (testWidth > maxTextWidth && n > 0) {
        // context.fillText(line, x, y);
        line = words[n] + ' ';
        textHeight += lineHeight;
      } else {
        line = testLine;
        if (testWidth > longestLine) {
          longestLine = testWidth;
        }
      }
    }
    return {
      height: textHeight + lineHeight / 2 + topMargin * 2,
      width: longestLine + leftMargin * 2
    };

  }

  private createBubblePath(wctx, width, height, tailWidth, orientation) {
    // var ctx = this.context;
    const ctx = wctx;
    const ih = Math.max(height - 100, 0);
    const iw = Math.max(width - 100, 0);
    const tw = tailWidth;

    // ctx.moveTo(x, y);

    ctx.beginPath();
    // Move to top
    ctx.moveTo(50 + tw, 0);
    // Arc to left edge
    ctx.quadraticCurveTo(0 + tw, 0, 0 + tw, 27.5);

    // Begin talk point
    ctx.quadraticCurveTo(-5 + tw, 40, 0, 45);
    // End talk point
    ctx.quadraticCurveTo(-10 + tw, 55, 0 + tw, 55);

    // Left expandy line gap
    ctx.lineTo(0 + tw, 55 + ih);
    // Arc to bottom
    ctx.quadraticCurveTo(0 + tw, 75 + ih, 41 + tw, 75 + ih);
    // Bottom expandy line gap
    ctx.lineTo(41 + iw + tw, 75 + ih);
    // Arc to right edge
    ctx.quadraticCurveTo(100 + iw + tw, 75 + ih, 100 + iw + tw, 37.5 + ih);
    // Right expandy line gap
    ctx.lineTo(100 + iw + tw, 36);
    // Arc to top
    ctx.quadraticCurveTo(100 + iw + tw, 0, 51 + iw + tw, 0);
    // Top expandy line gap
    ctx.lineTo(50 + tw, 0);
    ctx.closePath();
  }

  private strokeBubble(wctx: any, width: number, height: number, tailWidth: number, orientation: string) {
    // var ctx = this.context;
    // console.log(this.context.fillStyle);
    this.createBubblePath(wctx, width, height, tailWidth, orientation);
    wctx.stroke();
  }

  private fillBubble(wctx: any, width: number, height: number, tailWidth: number, orientation: string) {
    // var ctx = this.context;
    this.createBubblePath(wctx, width, height, tailWidth, orientation);
    wctx.fill();
  }

  private createImage(w: number, h: number) {
    // console.log('creating temp canvas');
    const image = document.createElement('canvas');
    // console.log(image);
    image.width = w;
    // console.log(image.width);
    image.height = h;
    // console.log(image.height);
    // console.log(image.getContext('2d'));
    // image.ctx = image.getContext("2d");
    return image;
  }

  private inOutStrokeBubble(width: number, height: number, tailWidth: number, orientation: string, strokeWidth: number, style: string, where: string) {
    //  clear the workspace
    const cw = (<HTMLCanvasElement>this.canvas.nativeElement).width;
    const ch = (<HTMLCanvasElement>this.canvas.nativeElement).height;
    const ctx = this.context;
    const workCtx = this.createImage(cw, ch);
    const wctx = workCtx.getContext('2d');
    // console.log('Got wctx');
    // console.log(wctx);
    wctx.globalCompositeOperation = 'source-over';
    wctx.clearRect(0, 0, workCtx.width, workCtx.height);

    // set the width to double
    wctx.lineWidth = strokeWidth * 2;
    wctx.strokeStyle = style;

    // fill colour does not matter here as its not seen
    wctx.fillStyle = 'white';

    // can use any join type
    wctx.lineJoin = 'round';

    // draw the shape outline at double width

    this.strokeBubble(wctx, width, height, tailWidth, orientation);

    // set comp to in.
    // in means leave only pixel that are both in the source and destination
    if (where.toLowerCase() === 'in') {
        wctx.globalCompositeOperation = 'destination-in';
    } else {
        // out means only pixels on the destination that are not part of the source
        wctx.globalCompositeOperation = 'destination-out';
    }
    this.fillBubble(wctx, width, height, tailWidth, orientation);
    // console.log(workCtx);
    ctx.drawImage(workCtx, 0, 0);
  }

  private wrapText(text: string, x: number, y: number, maxWidth: number, lineHeight: number) {
    const context = this.context;

    const words = text.split(' ');
    let line = '';

    for (let n = 0; n < words.length; n += 1) {
      const testLine = line + words[n] + ' ';
      const metrics = context.measureText(testLine);
      const testWidth = metrics.width;
      if (testWidth > maxWidth && n > 0) {
        context.fillText(line, x, y);
        line = words[n] + ' ';
        y += lineHeight;
      } else {
        line = testLine;
      }
    }
    context.fillText(line, x, y);
  }

  private renderSpeech(text: string = 'Hello!', offset: Offset = DEFAULT_OFFSET, dimensions?: Dimensions, orientation: string = 'left') {
    const ctx = this.context;
    const x = offset.x;
    const y = offset.y;
    const maxWidth = dimensions.width;
    ctx.font = '16pt ShadowsIntoLight';
      // this.context.font = '12px ShadowsIntoLight';

    ctx.fillStyle = '#fff';
    ctx.translate(x, y);
    const textMargin = {
      left: 25,
      top: 40
    };
    const lineHeight = 25;
    const tailWidth = 20;
    let textOffset = 0;

    const bubbleSize = this.calculateBubbleSize(text, maxWidth, lineHeight, textMargin.left, textMargin.top);
    // console.log(bubbleSize);
    if (orientation === 'left') {
      textOffset = tailWidth;
    }
    if (orientation === 'right') {
      // Flip the drawing direction
      textOffset = -(bubbleSize.width + tailWidth);
      ctx.scale(-1, 1);
    }
    this.fillBubble(ctx, bubbleSize.width, bubbleSize.height, tailWidth, orientation);
    this.inOutStrokeBubble(bubbleSize.width, bubbleSize.height, tailWidth, orientation, 20, 'rgb(211,237,247)', 'in');
    this.inOutStrokeBubble(bubbleSize.width, bubbleSize.height, tailWidth, orientation, 3, 'rgb(0,0,0)', 'in');


    if (orientation === 'right') {
      // Flip it back before rendering the text
      ctx.scale(-1, 1);
    }
    ctx.fillStyle = '#000';
    this.wrapText(text, textMargin.left + textOffset, textMargin.top, maxWidth - (2 * textMargin.left), lineHeight);

    // console.log('renderSpeech:', text);
  }

  /**
   * Render the current panel into the canvas
   */
  private render(parentOffset: Offset = DEFAULT_OFFSET) {
    if (!this.panel || !this.context) {
      return;
    }

    // console.log('render:', this.panel);

    // Prepare the layers for rendering, starting with the root layer
    const layerPromises: Promise<RenderDetails>[] = this.prepareLayer(this.panel.layer);

    // Render all the layers to the canvas
    Promise.all(layerPromises)
      .then(layers => {
        layers.forEach((layer: RenderDetails) => {
          // console.log('layer:', layer);
          if (layer.image) {
            this.context.drawImage(layer.image, layer.offset.x, layer.offset.y, layer.dimensions.width, layer.dimensions.height);
          }

          if (layer.text) {
            this.renderSpeech(layer.text, layer.offset, layer.dimensions);
          }
        });
        // this.renderSpeech(layer, DEFAULT_OFFSET, DEFAULT_TEXT_DIMENSIONS, "left");
      });

    // TODO: this should be done inside the rendering above
    // this.renderSpeech('hello world!');
  }

  /**
   * Recursvily load the given layer. Returns a list of promises that will resolve once the images are loaded.
   */
  private prepareLayer(layer: Layer, parentOffset: Offset = DEFAULT_OFFSET): Promise<RenderDetails>[] {
    // Do the initial render of each individual layers
    const layerPromises = [];

    // Compute the offsets for the current layer based on the parents offsets and the current layers offets
    const currentLayerOffset = layer.position ? offsets.get(layer.position) : DEFAULT_OFFSET;
    const computedOffset = {
      x: parentOffset.x + currentLayerOffset.x,
      y: parentOffset.y + currentLayerOffset.y
    };

    // Load the current layer
    if (layer.url) {
      layerPromises.push(this.loadLayer(layer.url, computedOffset));
    }

    if (layer.text) {
      layerPromises.push(Promise.resolve({
        text: layer.text,
        offset: {
          x: computedOffset.x,
          y: computedOffset.y + TEXT_Y_OFFSET
        },
        dimensions: DEFAULT_TEXT_DIMENSIONS
      }));
    }

    // If the layer has children, recursively load those layers with the currentLayer's offset as the parent
    if (layer.children) {
      layerPromises.push(
        ... flatMap(layer.children, childLayer => {
          const layerResults = this.prepareLayer(childLayer, computedOffset);
          return layerResults;
        })
      );
    }

    return layerPromises;
  }

  /**
   * Loads the individual layer
   * @param url
   * @param offset
   * @param dimensions
   */
  private loadLayer(url: string, offset?: Offset, dimensions?: Dimensions): Promise<RenderDetails> {
    return new Promise((resolve, reject) => {
      const image = new Image();
      image.onload = () => {

        // compute dimensions from loaded image
        dimensions = dimensions || { width: image.width, height: image.height };

        // TODO: HACK FOR BACKGROUND IMAGES
        if (dimensions.width === 900 || dimensions.width === 901) {
          dimensions = BACKGROUND_DIMESIONS;
        }

        // Image loaded and ready to be rendered, resolve the promise
        resolve({
          image,
          offset: offset || { x: 0, y: 0 },
          dimensions
        });
      };

      // Initiate the load
      image.src = ASSET_SERVER_URL + url;
    });
  }
}
