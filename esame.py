class ExamException(Exception):
    pass

class CSVTimeSeriesFile():
    def __init__(self, name):
        #controllo che il tipo di name sia una stringa
        if not isinstance(name,str):
            raise ExamException('Errore, name non è una stringa')
        self.name=name

    def get_data(self):
        #provo ad aprire il file e controllo che il file esista
        try:
            my_file=open(self.name, 'r')
            my_file.readline()
        except:
            raise ExamException('Errore, file non apribile')
            return None
        #inizializzo una lista vuota per salvare tutti i dati contenuti nel file
        time_series=[]
        #leggo il file linea per linea, faccio lo split di ogni riga sulla virgola in modo da separare l'epoch dalla temperatura
        for line in my_file:
            elements=line.split(',',1) #impostando il parametro maxsplit a 1, viene restituita una lista di soli due elementi, così che nel caso in cui la riga contenga più virgole, si considera solamente quella che separa l'epoch dalla temperatura
            #Pulisco il carattere di newline dall'ultimo elemento
            elements[-1]=elements[-1].strip()
            #se non sto processando l'intestazione...
            if elements[0]!='epoch':
                #controllo che ci siano almeno due elementi per ogni riga, ovvero l'epoch e la temperatura 
                if(len(elements)>=2):
                    epoch=elements[0]
                    temperature=elements[1]
                    
                    #Verifico che non ci siano linee incomplete o pezzi di testo che non centrano; se ci sono, salto la riga e passo alla successiva
                    #Verifico che l'epoch sia di tipo intero, se non lo è, lo converto ad intero e nel caso in cui ciò non fosse possibile, ignoro la riga e passo alla successiva tramite "continue"
                    try:
                        epoch=int(float(epoch))
                    except:
                        print('Errore,il timestamp epoch non è di tipo intero,ma di tipo:{}'.format(type(epoch)))
                        continue
                        
                    #Verifico che la temperatura sia di tipo numerico (intero o floating point); se non lo è, non accetto il valore e passo alla riga successiva
                    try:
                        temperature=float(temperature)
                    except:
                        print('Errore, il valore di temperatura non è di tipo numerico, ma di tipo:{}'.format(type(temperature)))
                        continue

                    #Verifico che la temperatura non sia ugaule a zero; se lo è salto la riga e passo a quella successiva  
                    if (temperature==0.0):
                        print('Errore, il valore di temperatura è zero')
                        continue
                        
                time_series.append([epoch,temperature])
        my_file.close()
        
        #ora ho tutti i dati "puliti"
        #creo una lista per salvere gli epoch
        list_epoch=[]
        
        for item in time_series:
            list_epoch.append(item[0]) #item[0] è il primo elemento di ogni sottoliista time_series e indica gli epoch 
    
        #controllo che il file non sia vuoto
        if len(list_epoch)==0:
            raise ExamException('Errore, il file inserito è vuoto')
        
        #controllo che non ci siano duplicati con la funzione count() che conta le occorrenze
        for item in list_epoch:
            if(list_epoch.count(item)>1):
                raise ExamException('Errore, il seguente epoch è ripetuto: {}'.format(item))
                
            if item not in range (1551398399,1554073201):
                raise ExamException('Errore, epoch fuori dal range assegnato:{}'.format(item))
                
        #controllo che la serie temporale sia ordinata
        #parto da i=1 saltando il primo elemento perchè non ho nessun dato precedente con cui confrontarlo
        i=1
        while i<(len(list_epoch)-1):
            if(list_epoch[i]<list_epoch[i-1]): 
                raise ExamException('Errore, la serie temporale non è ordinata in modo crescente')
            i=i+1   
            
        return (time_series)
        
def compute_daily_max_difference(time_series):
    temperatures=[] #lista vuota dove salvare tutte le temperature 
         
    previous_day=None #inizialmente gli assegno un valore impossibile, poi viene modificato. Gli avrei potuto dare anche valore -1
    for item in time_series: #scorro tutte le sottoliste di time_series
        temperatures_per_day=[] #sottolista vuota dove salvare le temperature rilevate per ogni giornata
        day_start_epoch=item[0]-(item[0]%86400) #trovo l'epoch di inizio giornata e tramite questa operazione, tutti gli epoch appartenenti al giorno corrente, saranno uguali a quello di inizio giornata 
        if(day_start_epoch!=previous_day):
            for list in time_series:
                if (list[0]-(list[0]%86400)==day_start_epoch): #se l'epoch che considero è uguale all'epoch di inizio giornata, appartiene al giorno corrente dunque aggiungo la rispettiva temperatura alla sottolista relativa al giorno corrente
                    temperatures_per_day.append(list[1]) 
            temperatures.append(temperatures_per_day)
        previous_day=day_start_epoch #setto il giorno precedente al giorno corrente 

        
    #di tutte le sottoliste devo trovare il valore max e min e farne la sottrazione così da trovare l'escursione termica giornaliera 

    result=[] #lista vuota che conterrà le escursioni termiche per ogni giornata 

    for temperatures_per_day in temperatures: #scorro tutte le sottoliste della lista_temp_giorno
        if len(temperatures_per_day)==1: #se una sottolista contiene solo un elemento ovvero per quella giornata è stata rilevata una sola temperatura, l'escursione termica non è definita, dunque, come da consegna, si aggiunge alla lista dei risultati il valore 'none' per quella giornata
            result.append('None')
        else: 
            result.append(max(temperatures_per_day)-min(temperatures_per_day))
    return ([result])