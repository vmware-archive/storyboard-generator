// Copyright © 2017-2018 VMware, Inc. All Rights Reserved.
// SPDX-License-Identifier: BSD-2-Clause

import { Component, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { StoryboardApi, Storyboard } from '../api/storyboard.api';
import { Subscription } from 'rxjs/Rx';

@Component({
    styleUrls: ['./home.component.scss'],
    templateUrl: './home.component.html',
})
export class HomeComponent implements OnDestroy {

  public storyboard: Storyboard;

  private _story: string = `# My First Story
Ethan: (blue, glasses, bronze skin) Hi I'm Ethan
Narrator: Ethan looks up the villain VM's owner, Jaime

SPLIT (phone)
Jaime: (orange, phone)
Ethan: (blue, glasses, bronze skin, phone)
Narrator: Ethan calls Jaime and explains the situation

OUTSIDE (desk)
Ethan:  It's okay to power off the vm
Narrator: Jaime tells Ethan the issue is being fixed and it's okay to restart the VM as a temporary workaround`;

  private paramsSubscription: Subscription;

  constructor(
    private api: StoryboardApi,
    private router: Router,
    private activeRoute: ActivatedRoute,
    private cd: ChangeDetectorRef
  ) {
    // Load the query params and update the story if it's been passed in
    this.paramsSubscription = this.activeRoute.queryParams.subscribe(params => {
      if (params.story) {
        console.log('params load:', params.story);
        this.story = atob(params.story);
        console.log('-- story:', this.story);
      }
    });
  }

  /** renders the current story into a storyboard */
  public renderStory() {
    if (this.story) {
      this.api.render(this._story)
        .then(storyboard => {
          if (storyboard.panels.length > 0) {
            this.storyboard = storyboard;
          }
        });
    }
  }

  public ngOnDestroy() {
    if (this.paramsSubscription) {
      this.paramsSubscription.unsubscribe();
    }
  }

  public get story(): string {
    return this._story;
  }

  public set story(story: string) {
    if (!story) {
      console.log('undefined');
      // No story to create
      this._story = '';
    } else {
      // Render the updated story
      this._story = story;
    }

    console.log('new story:', this.story);
    this.renderStory();

    // Update router state with new story
    this.router.navigate([''], {
      relativeTo: this.activeRoute,
      queryParams: { story: btoa(this.story) },
      replaceUrl: true
    });
  }

  public togglePreview() {
    let x = document.getElementById('home').className;
    if (x !== 'preview') {
      x = 'preview';
    } else {
      x = '';
    }
    document.getElementById('home').className = x;
  }

  public toggleInstructions() {
    let y = document.getElementById('editor').className;
    if (y !== 'max') {
      y = 'max';
    } else {
      y = '';
    }
    document.getElementById('editor').className = y;
  }

}
