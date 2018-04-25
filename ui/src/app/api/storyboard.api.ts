// Copyright © 2017-2018 VMware, Inc. All Rights Reserved.
// SPDX-License-Identifier: BSD-2-Clause

import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import { API_SERVER_URL } from '.';

export enum Position {
  LEFT, RIGHT, CENTER
}

export class Layer {
  url?: string;        // url for image
  position?: Position; // relative-to-parent position of layer
  type?: string;
  text?: string;       // for speech
  children?: Layer[];  // child layers
}

export class Panel {
  layer: Layer;
  caption?: string;
}

export class Storyboard {
  title: string;
  panels: Panel[];
}

@Injectable()
export class StoryboardApi {

  constructor(
    private http: Http
  ) {}

  public render(story: any): Promise<Storyboard> {

    // story-generator server endpoint
    const url = `${API_SERVER_URL}/render`;

    return new Promise((resolve, reject) => {
      this.http.post(url, story)
        .subscribe(response => {
          console.log('RESPONSE:', response.json());
          resolve(response.json());
        });
    });

    // return Promise.resolve({
    //   title: 'The Power of Love',
    //   panels: [{
    //     layer: {
    //       url: '/assets/ComputerScreenFront.png',
    //       children: [{
    //         text: 'hello world',
    //         position: Position.LEFT
    //       }, {
    //         url: '/assets/Bodies/body-green.png',
    //         position: Position.RIGHT,
    //         children: [{
    //           url: '/assets/Heads/head-bronze.png',
    //         }, {
    //           url: '/assets/Faces/face-confused.png',
    //         }, {
    //           url: '/assets/Accessories/bow-blue.png',
    //         }, {
    //           url: '/assets/Arms/arms-whatever.png',
    //         }]
    //       }]
    //     },
    //     caption: 'test'
    //   }]
    // });

  }
}
