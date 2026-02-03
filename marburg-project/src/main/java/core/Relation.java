/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package core;

import graphdb.Entity;
import java.util.LinkedHashMap;
import org.neo4j.driver.Session;
import org.neo4j.driver.TransactionWork;
import static org.neo4j.driver.Values.parameters;

/**
 *
 * @author AD\elahi_l
 */
public class Relation implements Constants {

    private String relationName = "";
    private String object_ID_1 = "";
    private String object_ID_2 = "";
    private String nodeType_1 = "";
    private String nodeType_2 = "";
    private boolean relationExisit = false;


    public Relation(String entityObjectID,LinkedHashMap<String, String> properties) {
        for (String attribute : properties.keySet()) {
            if (attribute.contains(RELATION)) {
                this.relationName = attribute.replace(RELATION, "");
                this.object_ID_1 = properties.get(attribute);
                this.object_ID_2 =entityObjectID;
                this.relationExisit = true;
            }
          
        }

    }

    public Relation() {
    }

    public Relation(String relationName, String object_ID_1, String object_ID_2) {
        this.relationName=relationName;
        this.object_ID_1=object_ID_1;
        this.object_ID_2=object_ID_2;
        this.relationExisit = true;
    }

    public Relation(String relationName, String object_ID_1, String object_ID_2, String nodeType1, String nodeType2) {
        this.relationName = relationName;
        this.object_ID_1 = object_ID_1;
        this.object_ID_2 = object_ID_2;
        this.relationExisit = true;
        this.nodeType_1 = nodeType1;
        this.nodeType_2 = nodeType2;
    }

    public String getRelationName() {
        return relationName;
    }

    public String getObject_ID_1() {
        return object_ID_1;
    }

    public String getObject_ID_2() {
        return object_ID_2;
    }

    public boolean isRelationExisit() {
        return relationExisit;
    }

    public String getNodeType_1() {
        return nodeType_1;
    }

    public String getNodeType_2() {
        return nodeType_2;
    }

    @Override
    public String toString() {
        return "Relation{" + "relationName=" + relationName + ", object_ID_1=" + object_ID_1 + ", object_ID_2=" + object_ID_2 + ", nodeType_1=" + nodeType_1 + ", nodeType_2=" + nodeType_2 + ", relationExisit=" + relationExisit + '}';
    }

   

   

    
}
