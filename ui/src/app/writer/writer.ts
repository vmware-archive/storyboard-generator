// Copyright © 2017-2018 VMware, Inc. All Rights Reserved.
// SPDX-License-Identifier: BSD-2-Clause

import { Component, Output, EventEmitter, Input, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import 'rxjs/add/operator/debounceTime';

const DEBOUNCE_TIME_MILLIS = 200;

@Component({
  selector: 'app-writer',
  templateUrl: './writer.html',
  styleUrls: ['./writer.scss']
})
export class WriterComponent implements OnInit {

  @Output() storyChange = new EventEmitter<string>();

  private _story: string;
  public storyControl = new FormControl();

  public ngOnInit() {
    // debounce keystroke events
    this.storyControl.valueChanges
      .debounceTime(DEBOUNCE_TIME_MILLIS)
      .subscribe(newStory => {
        console.log('story change:', newStory);
        this.story = newStory;
      });
  }

  public get story(): string {
    return this._story;
  }

  @Input()
  public set story(story: string) {
    this._story = story;
    this.storyChange.emit(this._story);
  }

}
