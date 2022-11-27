# Transportation Problem with Google ORTools


## Supuestos

Vamos a considerar:

- Indices
    - $d$: Número de Deposito
    - $l$: Número de Local
    - $n$: Número de producto

- Constantes:
    - $D$: Número total de Depósitos
    - $L$: Número total de Locales
    - $N$: Número total de Productos

- Limites:
    - $S$: Stock de los Depósitos
    - $T$: Demanda de los Locales  


***Variables:***

- $c^n_{dl}$  el costo de llevar el articulo n del Deposito _d_ al Local _l_ (números)

- $x^n_{dl}$  cantidad del articulo de llevar el articulo n del Deposito _d_ al Local _l_ (Entero)


Vamos a minizar el costo de entrega:

$$
    \min{\bigg(\sum^N_{n=1}\sum^D_{d=1}\sum^L_{l=1} c^n_{dl} x^n_{dl}}\bigg)
$$

***Restricciones:***

1. Las unidades enviadas tienen que ser positivas

$$
  x^n_{dl}\geq 0\, \forall l \, \forall d \, \forall n
$$

2. Se puede enviar como máximo el stock del depósito

$$
  \sum^L_{l=1}x^n_{dl}\leq S_d\, \forall d \, \forall n
$$


3. Se puede enviar como máximo la demanda de cada local

$$
  \sum^D_{d=1}x^n_{dl}\leq T_l\, \forall l \, \forall n
$$

4. Se debe enviar la demanda de cada local _l_

$$
  \sum^D_{d=1}x^n_{dl}\geq T_l\, \forall l \, \forall n
$$
