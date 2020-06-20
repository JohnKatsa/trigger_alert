import { Component, OnInit } from '@angular/core';
//import * as kRx from 'kafka-rxjs'

@Component({
  selector: 'app-kafka-consumer',
  templateUrl: './kafka-consumer.component.html',
  styleUrls: ['./kafka-consumer.component.css']
})
export class KafkaConsumerComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
    // kRx.consume({
    //   connectionString: 'localhost:2181',
    //   topics: [{topic: '11'}]
    // }).subscribe(function(message) {
    //   console.log(message)
    // })
  }

}
