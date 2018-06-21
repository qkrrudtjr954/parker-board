import { Component, OnInit } from '@angular/core';
import { BoardService } from '../../../services/board.service'
import {isUndefined} from "util";
import {Board, Boards} from "../../../models/board";
import {Pagination} from "../../../models/pagination";

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  boardlist: Board[];
  pagination: Pagination;

  constructor(private boardservice: BoardService) {
    this.getBoardList(10, 1)
  }

  getBoardList(per_page, page) {
    if(isUndefined(page) || page < 1){
      page = 1;
    }else if(!isUndefined(this.pagination) && page > this.pagination.pages){
      page = this.pagination.pages;
    }

    this.boardservice.getBoardList(per_page, page).subscribe((data: Boards) => {
      this.boardlist = data.boards;
      this.pagination = data.pagination;
    })
  }

  ngOnInit() { }

}
