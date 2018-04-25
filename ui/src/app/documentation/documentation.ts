// Copyright © 2017-2018 VMware, Inc. All Rights Reserved.
// SPDX-License-Identifier: BSD-2-Clause

import { Component, Output, EventEmitter } from '@angular/core';
import { CharacteristicsApi } from '../api/characteristics.api';

@Component({
  selector: 'app-documentation',
  templateUrl: './documentation.html',
  styleUrls: ['./documentation.scss']
})
export class DocumentationComponent {

  public characteristics = {};

  public locations = [];
  public bodies = [];
  public heads = [];

  constructor(
    private characteristicsApi: CharacteristicsApi
  ) {
    this.characteristicsApi.getCharacteristics().then(response => {
      this.characteristics = response;
      // console.log('characteristics:', this.characteristics);

      this.locations = this.extractTypes('location');
      this.bodies = this.extractTypes('body');
      this.heads = this.extractTypes('head');
      });
  }

  private extractTypes(type: string): any {
    const found = [];
    Object.keys(this.characteristics).map(key => {
      const values = <any[]>this.characteristics[key];
      const matchedValues = values.filter(v => v.type === type);

      if (matchedValues.length > 0) {
        found.push({
          type: key,
          values: matchedValues
        });
      }
    });
    return found;
  }
}
