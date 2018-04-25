// Copyright © 2017-2018 VMware, Inc. All Rights Reserved.
// SPDX-License-Identifier: BSD-2-Clause

import { BrowserModule } from '@angular/platform-browser';
import { HttpModule } from '@angular/http';
import { NgModule } from '@angular/core';
import { ClarityModule } from 'clarity-angular';
import { AppComponent } from './app.component';
import { WriterComponent } from './writer/writer';
import { InstructionsComponent } from './instructions/instructions';
import { StoryboardComponent } from './storyboard/storyboard';
import { PanelComponent } from './panel/panel';
import { StoryboardApi } from './api/storyboard.api';
import { ROUTING } from './app.routing';
import { HomeComponent } from './home/home.component';
import { DocumentationComponent } from './documentation/documentation';
import { ReactiveFormsModule } from '@angular/forms';
import { CharacteristicsApi } from './api/characteristics.api';

@NgModule({
  declarations: [
    AppComponent,
    WriterComponent,
    InstructionsComponent,
    StoryboardComponent,
    PanelComponent,
    HomeComponent,
    DocumentationComponent
  ],
  imports: [
    BrowserModule,
    HttpModule,
    ReactiveFormsModule,
    ClarityModule.forRoot(),
    ROUTING
  ],
  providers: [
    StoryboardApi,
    CharacteristicsApi
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
