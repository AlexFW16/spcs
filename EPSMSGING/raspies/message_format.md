### Message Format

##### Topic - Control
Sender: P1, Calc
Receiver: P1, Calc
```json

{"pressed":"0/1"}
```
this ^ is sent to Calc from P1

```json

{"state":"0/1/2/3"}
```
this ^ is sent to P1 from Calc

**States**\
0 = ¬Rain & ¬Dark = TTG: 10 & GD: 15\
1 = ¬Rain & Dark = TTG: 7 & GD: 10\
2 = Rain & ¬Dark = TTG: 7 & GD: 20\
3 = Rain & Dark = TTG: 5 & GD: 20

##### Topic - Data
Sender: P1, P2, Receiver; Calc
```json

{"humidity":"int or float?"}
```

```json
{"light":"int or float?"}
```

**States**\
0 = ¬Rain & ¬Dark = TTG: 10 & GD: 15\
1 = ¬Rain & Dark = TTG: 7 & GD: 10\
2 = Rain & ¬Dark = TTG: 7 & GD: 20\
3 = Rain & Dark = TTG: 5 & GD: 20
