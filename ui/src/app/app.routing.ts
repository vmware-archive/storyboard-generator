// Copyright © 2017-2018 VMware, Inc. All Rights Reserved.
// SPDX-License-Identifier: BSD-2-Clause

import { ModuleWithProviders } from '@angular/core/src/metadata/ng_module';
import { Routes, RouterModule } from '@angular/router';

import { DocumentationComponent } from './documentation/documentation';
import { HomeComponent } from './home/home.component';


export const ROUTES: Routes = [
    {path: '', redirectTo: 'home', pathMatch: 'full'},
    {path: 'home', component: HomeComponent},
    {path: 'documentation', component: DocumentationComponent}
];

export const ROUTING: ModuleWithProviders = RouterModule.forRoot(ROUTES);
