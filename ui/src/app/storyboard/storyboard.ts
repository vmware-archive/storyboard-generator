// Copyright © 2017-2018 VMware, Inc. All Rights Reserved.
// SPDX-License-Identifier: BSD-2-Clause

import { Component, Input } from '@angular/core';
import { Storyboard } from '../api/storyboard.api';

/**
 * Root level component for the Alerts page.
 */
@Component({
  selector: 'app-storyboard',
  templateUrl: './storyboard.html',
  styleUrls: ['./storyboard.scss']
})
export class StoryboardComponent {

  @Input() storyboard: Storyboard;
}
