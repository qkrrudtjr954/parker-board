import { NgModule } from '@angular/core';
import {IconCornerDownRight, IconHeart} from "angular-feather";

const icons = [
  IconHeart,
  IconCornerDownRight
];

@NgModule({
  exports: [icons]
})
export class IconsModule { }
