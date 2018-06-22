import { Component, OnInit } from '@angular/core';
import { BoardService } from '../../../services/board.service'
import { Board } from "../../../models/board";

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  boardlist: Board[];

  constructor(private boardservice: BoardService) {
    this.getBoardList()
  }

  getBoardList() {
    this.boardservice.getBoardList().subscribe((data: Board[]) => {
      console.log(data.length)
      this.boardlist = data;
    })
  }

  ngOnInit() { }

}
