// Copyright © 2017-2018 VMware, Inc. All Rights Reserved.
// SPDX-License-Identifier: BSD-2-Clause

import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  public showShareButton: boolean = true;

  constructor(
    private router: Router,
    private route: ActivatedRoute
  ) {
    // Show the share button if we're on the Story page.
    router.events.subscribe(() => {
      this.showShareButton = this.router.url.indexOf('/home') > -1;
    });
  }

  /** Generates a tinyurl for the current state of the storyboard */
  public generateTinyUrl() {
    const tinyUrl = `https://tinyurl.com/create.php?url=${window.location}`;
    window.open(tinyUrl, '_blank');
  }
}
